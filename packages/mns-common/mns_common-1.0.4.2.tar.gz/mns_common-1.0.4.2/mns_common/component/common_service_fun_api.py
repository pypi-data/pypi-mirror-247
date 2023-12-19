import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)

from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')

HUNDRED_MILLION = 100000000


def total_mv_classification(real_time_quotes_now):
    real_time_quotes_now['flow_mv_sp'] = round((real_time_quotes_now['flow_mv'] / HUNDRED_MILLION), 2)
    real_time_quotes_now['total_mv_sp'] = round((real_time_quotes_now['total_mv'] / HUNDRED_MILLION), 2)
    real_time_quotes_now['flow_mv_level'] = 0

    real_time_quotes_now.reset_index(drop=True, inplace=True)
    real_time_quotes_now.loc[(real_time_quotes_now["flow_mv_sp"] >= 0), ['flow_mv_level']] \
        = (real_time_quotes_now["flow_mv_sp"] // 10) + 1
    return real_time_quotes_now


# 股票分类
def classify_symbol(real_time_quotes_now_df):
    real_time_quotes_now_df['classification'] = real_time_quotes_now_df['symbol'].apply(
        lambda symbol: 'C' if symbol.startswith('3')
        else ('K' if symbol.startswith('68')
              else ('S' if symbol.startswith('0')
                    else ('X' if symbol.startswith('8') else ('X' if symbol.startswith('4') else "H")))))
    return real_time_quotes_now_df


# 单个股票分类
def classify_symbol_one(symbol):
    if symbol.startswith('3'):
        return 'C'
    elif symbol.startswith('68'):
        return 'K'
    elif symbol.startswith('0'):
        return 'S'
    elif symbol.startswith('4'):
        return 'X'
    elif symbol.startswith('8'):
        return 'X'
    else:
        return 'H'


def symbol_amount_simple(real_time_quotes_now_df):
    real_time_quotes_now_df['amount_level'] = round(real_time_quotes_now_df['amount'] / HUNDRED_MILLION, 2)
    return real_time_quotes_now_df


# 排除 新股
def exclude_new_stock(real_time_quotes_now_df):
    return real_time_quotes_now_df.loc[~(real_time_quotes_now_df['name'].str.contains('N'))]


# 排除st
def exclude_st_symbol(real_time_quotes_now_df):
    exclude_st_symbol_list = list(
        real_time_quotes_now_df.loc[(real_time_quotes_now_df['name'].str.contains('ST'))
                                    | (real_time_quotes_now_df['name'].str.contains('退'))]['symbol'])
    return real_time_quotes_now_df.loc[
        ~(real_time_quotes_now_df['symbol'].isin(
            exclude_st_symbol_list))]


# 排除b股数据
def exclude_b_symbol(real_time_quotes_now_df):
    return real_time_quotes_now_df.loc[(real_time_quotes_now_df.symbol.str.startswith('3'))
                                       | (real_time_quotes_now_df.symbol.str.startswith('0'))
                                       | (real_time_quotes_now_df.symbol.str.startswith('6'))
                                       | (real_time_quotes_now_df.symbol.str.startswith('4'))
                                       | (real_time_quotes_now_df.symbol.str.startswith('8'))]


def exclude_ts_symbol(real_time_quotes_now_df):
    return real_time_quotes_now_df.loc[~(real_time_quotes_now_df['name'].str.contains('退'))]


# 排除成交量为0 停牌的股票
def exclude_amount_zero_stock(real_time_quotes_now_df):
    return real_time_quotes_now_df.loc[~(real_time_quotes_now_df['amount'] == 0)]
