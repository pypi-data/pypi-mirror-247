import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

import pandas as pd
import mns_common.utils.date_handle_util as date_handle_util
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.api.em.east_money_stock_api as east_money_stock_api
from loguru import logger
import threading
import mns_common.component.trade_date.trade_date_common_service_api as trade_date_common_service_api
import mns_common.component.common_service_fun_api as common_service_fun_api
import mns_scheduler.k_line.sync.daily_week_month_line_sync as daily_week_month_line_sync_api
import mns_scheduler.k_line.clean.k_line_info_clean_impl as k_line_info_clean_impl

# 定义一个全局锁，用于保护 result 变量的访问
result_lock = threading.Lock()
# 初始化 result 变量为一个空的 Pandas DataFrame
result = pd.DataFrame()
# 分页大小
MAX_PAGE_NUMBER = 1000
mongodb_util = MongodbUtil('27017')


def sync_k_line_info_task(str_day):
    # 创建索引
    create_k_line_index()

    last_trade_day = trade_date_common_service_api.get_last_trade_day(str_day)
    query = {'date': date_handle_util.no_slash_date(last_trade_day)}
    count = mongodb_util.count(query, 'stock_qfq_daily')
    if count == 0:
        daily_week_month_line_sync_api.sync_all_daily_data('daily', 'qfq', 'stock_qfq_daily', str_day,
                                                           None)
    sync_k_line_info(str_day, None)


def sync_k_line_info(str_day, symbol_list):
    result_k_line_list_df = None
    if symbol_list is not None:
        for symbol in symbol_list:
            try:
                k_line_result = k_line_info_clean_impl.calculate_k_line_info(str_day, symbol)
                save_k_line_data(symbol, str_day, k_line_result)
                if result_k_line_list_df is None:
                    result_k_line_list_df = result
                else:
                    result_k_line_list_df = pd.concat([result_k_line_list_df, k_line_result])

            except BaseException as e:
                logger.error("k线同步错误:{},{},{}", str_day, symbol, e)
    else:
        result_k_line_list_df = multi_threaded_k_line_sync(str_day)
    logger.info("计算k线数据任务完成:{}", str_day)
    return result_k_line_list_df


# 多线程同步任务
def multi_threaded_k_line_sync(str_day):
    real_time_quotes_now = east_money_stock_api.get_real_time_quotes_all_stocks()
    #  exclude b symbol
    real_time_quotes_now = common_service_fun_api.exclude_b_symbol(real_time_quotes_now.copy())
    # exclude amount==0 symbol
    real_time_quotes_now = common_service_fun_api.exclude_amount_zero_stock(real_time_quotes_now)
    total_count = real_time_quotes_now.shape[0]
    global result
    result = pd.DataFrame()  # 重新初始化 result 变量
    threads = []
    page_number = round(total_count / MAX_PAGE_NUMBER, 0) + 1
    page_number = int(page_number)
    # 创建多个线程来获取数据
    for page in range(page_number):  # 0到page_number页
        logger.info("启动第{}个线程", page + 1)

        end_count = (page + 1) * MAX_PAGE_NUMBER
        begin_count = page * MAX_PAGE_NUMBER
        page_df = real_time_quotes_now.loc[begin_count:end_count]

        thread = threading.Thread(target=single_threaded_sync_task, args=(page_df, str_day, page))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 返回获取的接口数据
    return result


# 单线程同步任务
def single_threaded_sync_task(real_time_quotes_now, str_day, page):
    global result
    fail_symbol_list = []
    for stock_one in real_time_quotes_now.itertuples():
        try:
            k_line_df = k_line_info_clean_impl.calculate_k_line_info(str_day, stock_one.symbol)
            save_k_line_data(stock_one.symbol, str_day, k_line_df)
            if k_line_df is None:
                result = k_line_df
            else:
                result = pd.concat([k_line_df, result])
            # logger.info("k线清洗完成:{},{}", str_day, stock_one.symbol)
        except BaseException as e:
            fail_symbol_list.append(stock_one.symbol)
            logger.error("k线清洗错误:{},{},{}", str_day, stock_one.symbol, e)
    if len(fail_symbol_list) > 0:
        fail_symbol_data_df = real_time_quotes_now.loc[real_time_quotes_now['symbol'].isin(fail_symbol_list)]
        single_threaded_sync_task(fail_symbol_data_df, str_day, page)
    logger.info("k线数据清洗到:{}页", page + 1)
    return result


def save_k_line_data(symbol, str_day, k_line_info):
    k_line_info['_id'] = symbol + '_' + str_day
    mongodb_util.save_mongo(k_line_info, 'k_line_info')


# 创建索引
def create_k_line_index():
    mongodb_util.create_index('k_line_info', [("symbol", 1)])
    mongodb_util.create_index('k_line_info', [("str_day", 1)])
    mongodb_util.create_index('k_line_info', [("str_day", 1), ("symbol", 1)])


if __name__ == '__main__':
    sync_k_line_info_task("2023-12-17")
