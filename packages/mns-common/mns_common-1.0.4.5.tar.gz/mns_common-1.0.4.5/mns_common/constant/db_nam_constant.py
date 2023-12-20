import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 7
project_path = file_path[0:end]
sys.path.append(project_path)

BIG_DEAL_NAME = "ths_big_deal_fund"
BIG_DEAL_CHOOSE_NAME = "big_deal_fund_choose"
