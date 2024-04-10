# qmt_server.py
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from xtquant import xtdata
import requests
from datetime import datetime, timedelta
import json
import random
import time
import config
import pandas as pd

path = config.path
# session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
session_id = random.randint(0,9999999999)
xt_trader = XtQuantTrader(path, session_id)
account = StockAccount(config.account_id,config.account_type)
xt_trader.start()
# 建立交易连接，返回0表示连接成功
connect_result = xt_trader.connect()
if connect_result != 0:
    print(connect_result)
    import sys
    sys.exit('链接失败，程序即将退出 %d'%connect_result)

ret=xtdata.download_history_data(stock_code='000001.SZ', period='1m', start_time='20240401', end_time='20240410')
data = xtdata.get_local_data(field_list=[], stock_code=['000001.SZ'], period='1m', count=10)

print(ret)
print(data)