from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from xtquant import xtdata
import requests
from datetime import datetime, timedelta
import json
import random

def get_price(code):
    res = xtdata.get_full_tick([code])
    #print(res[code])        # {'timetag': '20240228 11:30:01', 'lastPrice': 1686, 'open': 1688.92, 'high': 1696.57, 'low': 1674.01, 'lastClose': 1689.5, 'amount': 3139981100, 'volume': 18649, 'pvolume': 1864909, 'stockStatus': 0, 'openInt': 13, 'settlementPrice': 0, 'lastSettlementPrice': 0, 'askPrice': [1688.5, 1688.53, 1688.84, 0, 0], 'bidPrice': [1686.12, 1686, 1685.26, 0, 0], 'askVol': [98, 3, 1, 0, 0], 'bidVol': [1, 1, 1, 0, 0]}
    return (res[code]['lastPrice'])



def get_daily_info(code):
    quote=xtdata.get_full_tick([code])
    detail=xtdata.get_instrument_detail(code)
    info={
          'ts_code':code,
          'open':quote[code]['open'],
          'high':quote[code]['high'],
          'low':quote[code]['low'],
          'close':quote[code]['lastPrice'],
          'volume':quote[code]['amount'],
          'amount':quote[code]['volume'],
          'name':detail['InstrumentName'],
          'vwap':0,
          'stop':detail['InstrumentStatus'],
          'up_limit':detail['UpStopPrice'],
          'down_limit':detail['DownStopPrice'],
    }
    return info



def subscribe(xt_trader,code):
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    subscribe_result = xt_trader.subscribe(acc)
    if subscribe_result != 0:
        print('账号订阅失败 %d'%subscribe_result)

    sub=xtdata.subscribe_whole_quote(['SH', 'SZ'], callback=None)
    print(1)
    xtdata.subscribe_quote(['002624'], period='1d', start_time='', end_time='', count=0, callback=None)
    print(2)
    try:
        x=xtdata.get_market_data(field_list=[], stock_list=['002624'], period='1d', start_time='', end_time='', count=-1, dividend_type='none', fill_data=True)
    except:
        print("------------------")
    print(3)
    print(x)
