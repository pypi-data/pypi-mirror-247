import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)

from functools import lru_cache
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.utils.date_handle_util as date_handle_util
import mns_common.api.akshare.stock_zt_pool_api as stock_zt_pool_api
import mns_common.component.trade_date.trade_date_common_service_api as trade_date_common_service_api

mongodb_util = MongodbUtil('27017')


@lru_cache(maxsize=None)
def get_last_trade_day_zt(str_day):
    last_trade_day = trade_date_common_service_api.get_last_trade_day(str_day)
    query = {'str_day': last_trade_day}
    db_stock_zt_pool = mongodb_util.find_query_data('stock_zt_pool', query)
    if db_stock_zt_pool is None or db_stock_zt_pool.shape[0] == 0:
        db_stock_zt_pool = stock_zt_pool_api.stock_em_zt_pool_df(date_handle_util.no_slash_date(last_trade_day))
    return db_stock_zt_pool


if __name__ == '__main__':
    get_last_trade_day_zt('20231215')
