#coding:utf-8

import datetime as dt
import threading
import time
import traceback

from xtquant import xtdata
from xtquant import xtbson as bson

_request_id = ''

def datetime_to_timetag(timelabel, format = ''):
    '''
    timelabel: str '20221231' '20221231235959'
    format: str '%Y%m%d' '%Y%m%d%H%M%S'
    return: int 1672502399000
    '''
    if not format:
        format = '%Y%m%d' if len(timelabel) == 8 else '%Y%m%d%H%M%S'
    return dt.datetime.strptime(timelabel, format).timestamp() * 1000

def timetag_to_datetime(timetag, format = ''):
    '''
    timetag: int 1672502399000
    format: str '%Y%m%d' '%Y%m%d%H%M%S'
    return: str '20221231' '20221231235959'
    '''
    if not format:
        format = '%Y%m%d' if timetag % 86400000 == 57600000 else '%Y%m%d%H%M%S'
    return dt.datetime.fromtimestamp(timetag / 1000).strftime(format)

def subscribe_quote(stock_code, period, dividend_type, result_type = '', callback = None):
    return xtdata.subscribe_quote(stock_code, period, '', '', 0, callback)

def subscribe_whole_quote(code_list, callback = None):
    return xtdata.subscribe_whole_quote(code_list, callback)

def unsubscribe_quote(subscribe_id):
    return xtdata.unsubscribe_quote(subscribe_id)

def get_market_data(
    fields = [], stock_code = [], start_time = '', end_time = ''
    , skip_paused = True, period = '', dividend_type = '', count = -1
):
    res = {}
    if period == 'tick':
        refixed = False
        if count == -2:
            refixed = True
            count = 1
        if 'quoter' not in fields:
            return xtdata.get_market_data_ori(
                    field_list=fields, stock_list=stock_code, period=period
                    , start_time=start_time, end_time=end_time, count=count
                    , dividend_type=dividend_type, fill_data=skip_paused
                )

        fields = []
        data = xtdata.get_market_data_ori(
            field_list=fields, stock_list=stock_code, period=period
            , start_time=start_time, end_time=end_time, count=count
            , dividend_type=dividend_type, fill_data=skip_paused
        )
        fields = ['quoter']

        import pandas as pd

        stime_fmt = '%Y%m%d' if period == '1d' else '%Y%m%d%H%M%S'
        for stock in data:
            pd_data = pd.DataFrame(data[stock])
            pd_data['stime'] = [timetag_to_datetime(t, stime_fmt) for t in pd_data['time']]
            pd_data.index = pd.to_datetime((pd_data['time'] + 28800000) * 1000000)
            ans = {}
            for j, timetag in enumerate(pd_data['time']):
                d_map = {}
                for key in pd_data:
                    d_map[key] = pd_data[key][j]
                ans[str(pd_data.index[j])] = {}
                ans[str(pd_data.index[j])]['quoter'] = d_map
            res[stock] = ans

        oriData = res
            # if not pd_data.empty:
            #     if count > 0:
            #         return list(pd_data.T.to_dict().values())
            #     return pd_data.iloc[-1].to_dict()
            # return {}
        if refixed:
            count = -2
    else:
        refixed = False
        if count == -2:
            refixed = True
            count = 1
        index, data = xtdata.get_market_data_ori(
            field_list=fields, stock_list=stock_code, period=period
            , start_time=start_time, end_time=end_time, count=count
            , dividend_type=dividend_type, fill_data=skip_paused
        )
        if refixed:
            end_time = ''
            count = -1
        for i, stock in enumerate(index[0]):
            ans = {}
            for j, timetag in enumerate(index[1]):
                d_map = {}
                for key in data:
                    d_map[key] = data[key][i][j]
                ans[timetag] = d_map
            res[stock] = ans
        oriData = res

    resultDict = {}
    for code in oriData:
        for timenode in oriData[code]:
            values = []
            for field in fields:
                values.append(oriData[code][timenode][field])
            key = code + timenode
            resultDict[key] = values

    if len(fields) == 1 and len(stock_code) <= 1 and (
            (start_time == '' and end_time == '') or start_time == end_time) and (count == -1 or count == -2):
        # if resultDict:
            # keys = list(resultDict.keys())
            # if resultDict[keys[-1]]:
            #     return resultDict[keys[-1]]
        for key in resultDict:
            return resultDict[key][0]
        return -1
    import numpy as np
    import pandas as pd
    if len(stock_code) <= 1 and start_time == '' and end_time == '' and (count == -1 or count == -2):
        for key in resultDict:
            result = pd.Series(resultDict[key], index=fields)
            return result
    if len(stock_code) > 1 and start_time == '' and end_time == '' and (count == -1 or count == -2):
        values = []
        for code in stock_code:
            if code in oriData:
                if not oriData[code]:
                    values.append([np.nan])
                for timenode in oriData[code]:
                    key = code + timenode
                    values.append(resultDict[key])
            else:
                values.append([np.nan])
        result = pd.DataFrame(values, index=stock_code, columns=fields)
        return result
    if len(stock_code) <= 1 and ((start_time != '' or end_time != '') or count >= 0):
        values = []
        times = []
        for code in oriData:
            for timenode in oriData[code]:
                key = code + timenode
                times.append(timenode)
                values.append(resultDict[key])
        result = pd.DataFrame(values, index=times, columns=fields)
        return result
    if len(stock_code) > 1 and ((start_time != '' or end_time != '') or count >= 0):
        values = {}
        for code in stock_code:
            times = []
            value = []
            if code in oriData:
                for timenode in oriData[code]:
                    key = code + timenode
                    times.append(timenode)
                    value.append(resultDict[key])
            values[code] = pd.DataFrame(value, index=times, columns=fields)
        try:
            result = pd.Panel(values)
            return result
        except:
            return oriData
    return

def get_market_data_ex(
    fields = [], stock_code = [], period = ''
    , start_time = '', end_time = '', count = -1
    , dividend_type = '', fill_data = True, subscribe = True
):
    res = xtdata.get_market_data_ex(
        field_list = fields, stock_list = stock_code, period = period
        , start_time = start_time, end_time = end_time, count = count
        , dividend_type = dividend_type, fill_data = fill_data
    )
    for stock in res:
        res[stock]['stime'] = res[stock].index
    return res

def get_full_tick(stock_code):
    return xtdata.get_full_tick(stock_code)

def get_divid_factors(stock_code, date = None):
    client = xtdata.get_client()
    if date:
        data = client.get_divid_factors(stock_code, date, date)
    else:
        data = client.get_divid_factors(stock_code, '19700101', '20380119')

    res = {}
    for value in data.values():
        res[value['time']] = list(value.values())[1:]
    return res

def download_history_data(stockcode, period, startTime, endTime):
    return xtdata.download_history_data(stockcode, period, startTime, endTime)

def get_raw_financial_data(field_list, stock_list, start_date, end_date, report_type = 'announce_time'):
    client = xtdata.get_client()
    data = client.get_financial_data(stock_list, field_list, start_date, end_date, report_type)

    import time
    res = {}
    for stock in data:
        stock_data = data[stock]
        res[stock] = {}

        for field in field_list:
            fs = field.split('.')
            table_data = stock_data[fs[0]]

            ans = {}
            for row_data in table_data:
                date = time.strftime('%Y%m%d', time.localtime(row_data[report_type] / 1000))
                if start_date <= date <= end_date:
                    ans[int(row_data[report_type])] = row_data[fs[1]]
            res[stock][field] = ans
    return res

#def download_financial_data(stock_list, table_list): #暂不提供
#    return xtdata.download_financial_data(stock_list, table_list)

def get_instrument_detail(stock_code):
    return xtdata.get_instrument_detail(stock_code)

#def get_instrument_type(stock_code): #暂不提供
#    return xtdata.get_instrument_type(stock_code)

def get_trading_dates(stock_code, start_date, end_date, count = -1, period = '1d'):
    if period != '1d':
        return []
    market = stock_code.split('.')[0]
    trade_dates = xtdata.get_trading_dates(market, start_date, end_date)
    if count == -1:
        return trade_dates
    if count > 0:
        return trade_dates[-count:]
    return []

def get_stock_list_in_sector(sector_name):
    return xtdata.get_stock_list_in_sector(sector_name)

def download_sector_data():
    return xtdata.download_sector_data()

download_sector_weight = download_sector_data #compat

def _passorder_impl(
    optype, ordertype, accountid, ordercode
    , prtype, modelprice, volume, ordertime, requestid
):
    data = {}

    data['optype'] = optype
    data['ordertype'] = ordertype
    data['accountid'] = accountid
    data['ordercode'] = ordercode
    data['prtype'] = prtype
    data['modelprice'] = modelprice
    data['volume'] = volume
    data['ordertime'] = ordertime

    client = xtdata.get_client()
    client.callFormula(requestid, 'passorder', bson.BSON.encode(data))
    return

def passorder(opType, orderType, accountid, orderCode, prType, modelprice, volume, C):
    return C.passorder(opType, orderType, accountid, orderCode, prType, modelprice, volume)

def get_trade_detail_data(accountid, accounttype, datatype, strategyname = ''):

    data = {}

    data['accountid'] = accountid
    data['accounttype'] = accounttype
    data['datatype'] = datatype
    data['strategyname'] = strategyname

    client = xtdata.get_client()
    result_bson = client.callFormula(_request_id, 'gettradedetail', bson.BSON.encode(data))
    result = bson.BSON.decode(result_bson)

    class DetailData(object):
        def __init__(self, _obj):
            if _obj:
                self.__dict__.update(_obj)

    out = []
    for item in result.get('result'):
        out.append(DetailData(item))
    return out

def register_external_resp_callback(reqid, callback):
    client = xtdata.get_client()

    status = [False, 0, 1, '']

    def on_callback(type, data, error):
        try:
            result = bson.BSON.decode(data)
            callback(type, result, error)
            return True
        except:
            status[0] = True
            status[3] = 'exception'
            return True

    client.register_external_resp_callback(reqid, on_callback)

def _set_auto_trade_callback_impl(enable, requestid):
    data = {}
    data['enable'] = enable

    client = xtdata.get_client()
    client.callFormula(requestid, 'setautotradecallback', bson.BSON.encode(data))
    return

def set_auto_trade_callback(C,enable):
    return C.set_auto_trade_callback(enable)

def set_account(accountid, requestid):
    data = {}
    data['accountid'] = accountid

    client = xtdata.get_client()
    client.callFormula(requestid, 'setaccount', bson.BSON.encode(data))
    return

def _get_callback_cache_impl(type, requestid):
    data = {}

    data['type'] = type

    client = xtdata.get_client()
    result_bson = client.callFormula(requestid, 'getcallbackcache', bson.BSON.encode(data))
    return bson.BSON.decode(result_bson)

def get_account_callback_cache(data, C):
    data = C.get_callback_cache("account").get('')
    return

def get_order_callback_cache(data, C):
    data = C.get_callback_cache("order")
    return

def get_deal_callback_cache(data, C):
    data = C.get_callback_cache("deal")
    return

def get_position_callback_cache(data, C):
    data = C.get_callback_cache("position")
    return

def get_ordererror_callback_cache(data, C):
    data = C.get_callback_cache("ordererror")
    return

