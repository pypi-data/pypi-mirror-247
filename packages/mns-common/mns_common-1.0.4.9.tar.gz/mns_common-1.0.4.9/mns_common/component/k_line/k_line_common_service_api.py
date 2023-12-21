import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)

import mns_common.component.k_line.pattern_Enum as pattern_Enum


def k_line_patterns_classify(open, close, high, low, max_chg, chg):
    if cross_star(open, close, high, low):
        return pattern_Enum.Pattern_Enum.CROSS_STAR
    elif down_over_lining(open, close, high, low):
        return pattern_Enum.Pattern_Enum.DOWN_OVER_LINING

    elif open_high_and_walk_low(open, close, high, low, max_chg, chg):
        return pattern_Enum.Pattern_Enum.OPEM_HIGH_AND_WALK_LOW

    elif up_over_lining(open, close, high, low):
        return pattern_Enum.Pattern_Enum.UP_OVER_LINING

    return pattern_Enum.Pattern_Enum.OTHER


# 十字星状态
def cross_star(open, close, high, low):
    if abs(open - close) < 0.01 * open and (high - max(open, close)) > 2 * (max(open, close) - min(open, close)) and (
            min(open, close) - low) > 2 * (max(open, close) - min(open, close)):
        return True
    else:
        return False


# 高开低走
def open_high_and_walk_low(open, close, high, low, max_chg, chg):
    if open > close and max_chg >= 7 and max_chg - chg >= 7:
        return True
    else:
        return False


# 下跌带长上影线
def down_over_lining(open, close, high, low):
    diff_chg_high = round((high - open) / open, 2)
    if open > close and diff_chg_high >= 7:
        return True
    else:
        return False


# 上涨带长上影线
def up_over_lining(open, close, high, low):
    diff_chg_high = round((high - open) / open, 2)
    if open < close and diff_chg_high >= 7:
        return True
    else:
        return False


# 计算k线相关参数 当前最大涨幅  回落的幅度 超平均价幅度
def calculate_real_time_k_line_param(real_time_quotes_now):
    # 最大涨幅
    real_time_quotes_now['max_chg'] = round(
        (((real_time_quotes_now['high'] - real_time_quotes_now['yesterday_price']) / real_time_quotes_now[
            'yesterday_price']) * 100), 2)
    # 最大涨幅与当前涨幅的差值 越大表明是拉高出货
    real_time_quotes_now['chg_fall_back'] = round(real_time_quotes_now['max_chg'] - real_time_quotes_now['chg'], 2)
    # 当前价格与今天开盘价格的差值 为负表明为下跌趋势
    real_time_quotes_now['chg_from_open'] = round(
        (((real_time_quotes_now['now_price'] - real_time_quotes_now['open']) / real_time_quotes_now[
            'open']) * 100), 2)

    if 'average_price' in real_time_quotes_now.columns:
        # 高于平均线的差值 越大表明极速拉伸
        real_time_quotes_now['diff_avg_chg'] = round(
            (((real_time_quotes_now['now_price'] - real_time_quotes_now['average_price']) / real_time_quotes_now[
                'average_price']) * 100), 2)
    else:
        real_time_quotes_now['diff_avg_chg'] = 0
    return real_time_quotes_now
