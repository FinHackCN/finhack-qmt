#coding=utf-8
import asyncio
import os
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, Future
from . import xtpythonclient as XTQC
from . import xttype

def title(s = None):
    import inspect
    if not s:
        s = inspect.stack()[1].function
    print('-' * 33 + s + '-' * 33)
    return

def cp(s = None):
    import inspect
    st = inspect.stack()
    pos = {'title':st[1].function, 'line':st[1].lineno}
    print('-' * 33 + f'{pos}, {s}' + '-' * 33)
    return

# 交易回调类
class XtQuantTraderCallback(object):
    def on_connected(self):
        """
        连接成功推送
        """
        pass
        
    def on_disconnected(self):
        """
        连接断开推送
        """
        pass

    def on_account_status(self, status):
        """
        :param status: XtAccountStatus对象
        :return:
        """
        pass

    def on_stock_asset(self, asset):
        """
        :param asset: XtAsset对象
        :return:
        """
        pass

    def on_stock_order(self, order):
        """
        :param order: XtOrder对象
        :return:
        """
        pass

    def on_stock_trade(self, trade):
        """
        :param trade: XtTrade对象
        :return:
        """
        pass

    def on_stock_position(self, position):
        """
        :param position: XtPosition对象
        :return:
        """
        pass

    def on_order_error(self, order_error):
        """
        :param order_error: XtOrderError 对象
        :return:
        """
        pass

    def on_cancel_error(self, cancel_error):
        """
        :param cancel_error:XtCancelError 对象
        :return:
        """
        pass

    def on_order_stock_async_response(self, response):
        """
        :param response: XtOrderResponse 对象
        :return:
        """
        pass
    
    def on_smt_appointment_async_response(self, response):
        """
        :param response: XtAppointmentResponse 对象
        :return:
        """
        pass
    
    def on_cancel_order_stock_async_response(self, response):
        """
        :param response: XtCancelOrderResponse 对象
        :return:
        """
        pass

class XtQuantTrader(object):
    def __init__(self, path, session, callback=None):
        """
        :param path: mini版迅投极速交易客户端安装路径下，userdata文件夹具体路径
        :param session: 当前任务执行所属的会话id
        :param callback: 回调方法
        """
        self.async_client = XTQC.XtQuantAsyncClient(path.encode('gb18030'), 'xtquant', session)
        self.callback = callback

        self.connected = False

        self.oldloop = asyncio.get_event_loop()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.cbs = {}

        self.executor = None
        self.resp_executor = None

        self.relaxed_resp_order_enabled = False
        self.relaxed_resp_executor = None

        self.handled_async_order_stock_order_id = set()
        self.sync_order_stock_order_id = set()
        self.queuing_order_errors = {}

        self.handled_async_smt_appointment_order_id = set()
        self.sync_smt_appointment_order_id = set()
         
        self.handled_async_cancel_order_stock_order_id = set()
        self.handled_async_cancel_order_stock_order_sys_id = set()
        self.handled_sync_cancel_order_stock_order_id = set()
        self.handled_sync_cancel_order_stock_order_sys_id = set()
        self.queuing_cancel_errors_by_order_id = {}
        self.queuing_cancel_errors_by_order_sys_id = {}
        
        
    #########################
        #push
        def on_common_push_callback_wrapper(argc, callback):
            if argc == 0:
                def on_push_data():
                    self.executor.submit(callback)
                return on_push_data
            elif argc == 1:
                def on_push_data(data):
                    self.executor.submit(callback, data)
                return on_push_data
            elif argc == 2:
                def on_push_data(data1, data2):
                    self.executor.submit(callback, data1, data2)
                return on_push_data
            else:
                return None
        
        #response
        def on_common_resp_callback(seq, resp):
            callback = self.cbs.pop(seq, None)
            if callback:
                self.resp_executor.submit(callback, resp)
            return
        
        self.async_client.bindOnSubscribeRespCallback(on_common_resp_callback)
        self.async_client.bindOnUnsubscribeRespCallback(on_common_resp_callback)
        self.async_client.bindOnQueryStockAssetCallback(on_common_resp_callback)
        self.async_client.bindOnQueryStockOrdersCallback(on_common_resp_callback)
        self.async_client.bindOnQueryStockTradesCallback(on_common_resp_callback)
        self.async_client.bindOnQueryStockPositionsCallback(on_common_resp_callback)
        self.async_client.bindOnQueryCreditDetailRespCallback(on_common_resp_callback)
        self.async_client.bindOnQueryStkCompactsRespCallback(on_common_resp_callback)
        self.async_client.bindOnQueryCreditSubjectsRespCallback(on_common_resp_callback)
        self.async_client.bindOnQueryCreditSloCodeRespCallback(on_common_resp_callback)
        self.async_client.bindOnQueryCreditAssureRespCallback(on_common_resp_callback)
        self.async_client.bindOnQueryNewPurchaseLimitCallback(on_common_resp_callback)
        self.async_client.bindOnQueryIPODataCallback(on_common_resp_callback)
        self.async_client.bindOnQueryAppointmentInfoRespCallback(on_common_resp_callback)
        self.async_client.bindOnQuerySMTSecuInfoRespCallback(on_common_resp_callback)
        self.async_client.bindOnQuerySMTSecuRateRespCallback(on_common_resp_callback)
        
        self.async_client.bindOnQueryAccountInfosCallback(on_common_resp_callback)
        self.async_client.bindOnQueryAccountStatusCallback(on_common_resp_callback)
    #########################
        
        enable_push = 1
        
        #order push
        
        def on_push_SmtAppointmentAsyncResponse(seq, resp):
            callback = self.cbs.pop(seq, None)
            if callback:
                resp = xttype.XtAppointmentResponse(resp.m_strAccountID, resp.m_nOrderID, resp.m_nErrorID, resp.m_strErrorMsg, seq)
                callback(resp)
                self.handled_async_smt_appointment_order_id.add(resp.order_id)
            return
        
        if enable_push:
            self.async_client.bindOnSmtAppointmentRespCallback(on_common_push_callback_wrapper(2, on_push_SmtAppointmentAsyncResponse))
        
        def on_push_OrderStockAsyncResponse(seq, resp):
            callback = self.cbs.pop(seq, None)
            if callback:
                resp = xttype.XtOrderResponse(resp.m_strAccountID, resp.m_nOrderID, resp.m_strStrategyName, resp.m_strOrderRemark, resp.m_strErrorMsg, seq)
                callback(resp)
                self.handled_async_order_stock_order_id.add(resp.order_id)
                e = self.queuing_order_errors.pop(resp.order_id, None)
                if e is not None:
                    self.callback.on_order_error(e)
                    self.handled_async_order_stock_order_id.discard(resp.order_id)
            return
        
        if enable_push:
            self.async_client.bindOnOrderStockRespCallback(on_common_push_callback_wrapper(2, on_push_OrderStockAsyncResponse))
        
        def on_push_CancelOrderStockAsyncResponse(seq, resp):
            callback = self.cbs.pop(seq, None)
            if callback:
                resp = xttype.XtCancelOrderResponse(resp.m_strAccountID, resp.m_nCancelResult, resp.m_nOrderID, resp.m_strOrderSysID, seq)
                callback(resp)
                
                if not resp.order_sysid:
                    self.handled_async_cancel_order_stock_order_id.add(resp.order_id)
                    e = self.queuing_cancel_errors_by_order_id.pop(resp.order_id, None)
                    if e is not None:
                        self.handled_async_cancel_order_stock_order_id.discard(resp.order_id)
                        self.callback.on_cancel_error(e)
                else:
                    self.handled_async_cancel_order_stock_order_sys_id.add(resp.order_sysid)
                    e = self.queuing_cancel_errors_by_order_sys_id.pop(resp.order_sysid, None)
                    if e is not None:
                        self.handled_async_cancel_order_stock_order_sys_id.discard(resp.order_sysid)
                        self.callback.on_cancel_error(e)
            return
        
        if enable_push:
            self.async_client.bindOnCancelOrderStockRespCallback(on_common_push_callback_wrapper(2, on_push_CancelOrderStockAsyncResponse))
            
        def on_push_disconnected():
            if self.callback:
                self.callback.on_disconnected()

        if enable_push:
            self.async_client.bindOnDisconnectedCallback(on_common_push_callback_wrapper(0, on_push_disconnected))

        def on_push_AccountStatus(data):
            data = xttype.XtAccountStatus(data.m_strAccountID, data.m_nAccountType, data.m_nStatus)
            self.callback.on_account_status(data)

        if enable_push:
            self.async_client.bindOnUpdateAccountStatusCallback(on_common_push_callback_wrapper(1, on_push_AccountStatus))

        def on_push_StockAsset(data):
            self.callback.on_stock_asset(data)

        if enable_push:
            self.async_client.bindOnStockAssetCallback(on_common_push_callback_wrapper(1, on_push_StockAsset))

        def on_push_OrderStock(data):
            self.callback.on_stock_order(data)

        if enable_push:
            self.async_client.bindOnStockOrderCallback(on_common_push_callback_wrapper(1, on_push_OrderStock))

        def on_push_StockTrade(data):
            self.callback.on_stock_trade(data)

        if enable_push:
            self.async_client.bindOnStockTradeCallback(on_common_push_callback_wrapper(1, on_push_StockTrade))

        def on_push_StockPosition(data):
            self.callback.on_stock_position(data)

        if enable_push:
            self.async_client.bindOnStockPositionCallback(on_common_push_callback_wrapper(1, on_push_StockPosition))

        def on_push_OrderError(data):
            if data.order_id in self.handled_async_order_stock_order_id or data.order_id in self.sync_order_stock_order_id:
                self.handled_async_order_stock_order_id.discard(data.order_id)
                self.sync_order_stock_order_id.discard(data.order_id)
                self.callback.on_order_error(data)
            else:
                self.queuing_order_errors[data.order_id] = data

        if enable_push:
            self.async_client.bindOnOrderErrorCallback(on_common_push_callback_wrapper(1, on_push_OrderError))

        def on_push_CancelError(data):
            if not data.order_sysid:
                if data.order_id in self.handled_async_cancel_order_stock_order_id or data.order_id in self.handled_sync_cancel_order_stock_order_id:
                    self.handled_async_cancel_order_stock_order_id.discard(data.order_id)
                    self.handled_sync_cancel_order_stock_order_id.discard(data.order_id)
                    self.callback.on_cancel_error(data)
                else:
                    self.queuing_cancel_errors_by_order_id[data.order_id] = data
            else:
                if data.order_sysid in self.handled_async_cancel_order_stock_order_sys_id or data.order_sysid in self.handled_sync_cancel_order_stock_order_sys_id:
                    self.handled_async_cancel_order_stock_order_sys_id.discard(data.order_sysid)
                    self.handled_sync_cancel_order_stock_order_sys_id.discard(data.order_sysid)
                    self.callback.on_cancel_error(data)
                else:
                    self.queuing_cancel_errors_by_order_sys_id[data.order_sysid] = data

        if enable_push:
            self.async_client.bindOnCancelErrorCallback(on_common_push_callback_wrapper(1, on_push_CancelError))
        
    ########################

    def common_op_async_with_seq(self, seq, callable, callback):
        self.cbs[seq] = callback

        def apply(func, *args):
            return func(*args)
        apply(*callable)

        return seq

    def common_op_sync_with_seq(self, seq, callable):
        future = Future()
        self.cbs[seq] = lambda resp:future.set_result(resp)

        def apply(func, *args):
            return func(*args)
        apply(*callable)

        return future.result()

    #########################
    
    
    def __del__(self):
        if hasattr(self, 'oldloop'):
            asyncio.set_event_loop(self.oldloop)

    def register_callback(self, callback):
        self.callback = callback

    def start(self):
        self.async_client.init()
        self.async_client.start()
        self.executor = ThreadPoolExecutor(max_workers = 1)
        self.relaxed_resp_executor = ThreadPoolExecutor(max_workers = 1)
        self.resp_executor = self.relaxed_resp_executor if self.relaxed_resp_order_enabled else self.executor
        return

    def stop(self):
        self.async_client.stop()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.executor.shutdown(wait = True)
        self.relaxed_resp_executor.shutdown(wait = True)
        return

    def connect(self):
        result = self.async_client.connect()
        self.connected = result == 0
        return result

    def sleep(self, time):
        async def sleep_coroutine(time):
            await asyncio.sleep(time)
        asyncio.run_coroutine_threadsafe(sleep_coroutine(time), self.loop).result()

    def run_forever(self):
        import time
        while True:
            time.sleep(0.2)
        return

    def set_relaxed_response_order_enabled(self, enabled):
        self.relaxed_resp_order_enabled = enabled
        self.resp_executor = self.relaxed_resp_executor if self.relaxed_resp_order_enabled else self.executor
        return

    def subscribe(self, account):
        req = XTQC.SubscribeReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.subscribeWithSeq, seq, req)
        )

    def unsubscribe(self, account):
        req = XTQC.UnsubscribeReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.unsubscribeWithSeq, seq, req)
        )

    def order_stock_async(self, account, stock_code, order_type, order_volume, price_type, price, strategy_name='',
                          order_remark=''):
        """
        :param account: 证券账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param order_type: 委托类型, 23:买, 24:卖
        :param order_volume: 委托数量, 股票以'股'为单位, 债券以'张'为单位
        :param price_type: 报价类型, 详见帮助手册
        :param price: 报价价格, 如果price_type为指定价, 那price为指定的价格, 否则填0
        :param strategy_name: 策略名称
        :param order_remark: 委托备注
        :return: 返回下单请求序号, 成功委托后的下单请求序号为大于0的正整数, 如果为-1表示委托失败
        """
        req = XTQC.OrderStockReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_strStockCode = stock_code
        req.m_nOrderType = order_type
        req.m_nOrderVolume = order_volume
        req.m_nPriceType = price_type
        req.m_dPrice = price
        req.m_strStrategyName = strategy_name
        req.m_strOrderRemark = order_remark

        seq = self.async_client.nextSeq()
        self.cbs[seq] = self.callback.on_order_stock_async_response
        self.async_client.orderStockWithSeq(seq, req)
        return seq

    def order_stock(self, account, stock_code, order_type, order_volume, price_type, price, strategy_name='',
                          order_remark=''):
        """
        :param account: 证券账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param order_type: 委托类型, 23:买, 24:卖
        :param order_volume: 委托数量, 股票以'股'为单位, 债券以'张'为单位
        :param price_type: 报价类型, 详见帮助手册
        :param price: 报价价格, 如果price_type为指定价, 那price为指定的价格, 否则填0
        :param strategy_name: 策略名称
        :param order_remark: 委托备注
        :return: 返回下单请求序号, 成功委托后的下单请求序号为大于0的正整数, 如果为-1表示委托失败
        """
        req = XTQC.OrderStockReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_strStockCode = stock_code
        req.m_nOrderType = order_type
        req.m_nOrderVolume = order_volume
        req.m_nPriceType = price_type
        req.m_dPrice = price
        req.m_strStrategyName = strategy_name
        req.m_strOrderRemark = order_remark
        
        seq = self.async_client.nextSeq()
        resp = self.common_op_sync_with_seq(
            seq,
            (self.async_client.orderStockWithSeq, seq, req)
        )
        self.sync_order_stock_order_id.add(resp.order_id)
        return resp.order_id

    def cancel_order_stock(self, account, order_id):
        """
        :param account: 证券账号
        :param order_id: 委托编号, 报单时返回的编号
        :return: 返回撤单成功或者失败, 0:成功,  -1:委托已完成撤单失败, -2:未找到对应委托编号撤单失败, -3:账号未登陆撤单失败
        """
        req = XTQC.CancelOrderStockReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_nOrderID = order_id
        
        seq = self.async_client.nextSeq()
        resp = self.common_op_sync_with_seq(
            seq,
            (self.async_client.cancelOrderStockWithSeq, seq, req)
        )
        self.handled_sync_cancel_order_stock_order_id.add(resp.order_id)
        return resp.cancel_result

    def cancel_order_stock_async(self, account, order_id):
        """
        :param account: 证券账号
        :param order_id: 委托编号, 报单时返回的编号
        :return: 返回撤单请求序号, 成功委托后的撤单请求序号为大于0的正整数, 如果为-1表示委托失败
        """
        req = XTQC.CancelOrderStockReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_nOrderID = order_id
        
        seq = self.async_client.nextSeq()
        self.cbs[seq] = self.callback.on_cancel_order_stock_async_response
        self.async_client.cancelOrderStockWithSeq(seq, req)
        return seq

    def cancel_order_stock_sysid(self, account, market, sysid):
        """
        :param account:证券账号
        :param market: 交易市场 0:上海 1:深圳
        :param sysid: 柜台合同编号
        :return:返回撤单成功或者失败, 0:成功,  -1:撤单失败
        """
        req = XTQC.CancelOrderStockReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_nMarket = market
        req.m_strOrderSysID = sysid
        
        seq = self.async_client.nextSeq()
        resp = self.common_op_sync_with_seq(
            seq,
            (self.async_client.cancelOrderStockWithSeq, seq, req)
        )
        self.handled_sync_cancel_order_stock_order_sys_id.add(resp.order_sysid)
        return resp.cancel_result

    def cancel_order_stock_sysid_async(self, account, market, sysid):
        """
        :param account:证券账号
        :param market: 交易市场 0:上海 1:深圳
        :param sysid: 柜台编号
        :return:返回撤单请求序号, 成功委托后的撤单请求序号为大于0的正整数, 如果为-1表示委托失败
        """
        req = XTQC.CancelOrderStockReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_nMarket = market
        req.m_strOrderSysID = sysid
        
        seq = self.async_client.nextSeq()
        self.cbs[seq] = self.callback.on_cancel_order_stock_async_response
        self.async_client.cancelOrderStockWithSeq(seq, req)
        return seq

    def query_account_infos(self):
        """
        :return: 返回账号列表
        """
        req = XTQC.QueryAccountInfosReq()
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryAccountInfosWithSeq, seq, req)
        )
        
    query_account_info = query_account_infos
    
    def query_account_infos_async(self, callback):
        """
        :return: 返回账号列表
        """
        req = XTQC.QueryAccountInfosReq()
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryAccountInfosWithSeq, seq, req)
            , callback
        )
        
    def query_account_status(self):
        """
        :return: 返回账号状态
        """
        req = XTQC.QueryAccountStatusReq()
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryAccountStatusWithSeq, seq, req)
        )
    
    def query_account_status_async(self, callback):
        """
        :return: 返回账号状态
        """
        req = XTQC.QueryAccountStatusReq()
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryAccountStatusWithSeq, seq, req)
            , callback
        )

    def query_stock_asset(self, account):
        """
        :param account: 证券账号
        :return: 返回当前证券账号的资产数据
        """
        req = XTQC.QueryStockAssetReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        resp = self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStockAssetWithSeq, seq, req)
        )

        if resp and len(resp):
            return resp[0]
        return None
    
    def query_stock_asset_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回当前证券账号的资产数据
        """
        req = XTQC.QueryStockAssetReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        def _cb(resp):
            callback(resp[0] if resp else None)
        resp = self.common_op_async_with_seq(
            seq,
            (self.async_client.queryStockAssetWithSeq, seq, req)
            , _cb
        )
        return

    def query_stock_order(self, account, order_id):
        """
        :param account: 证券账号
        :param order_id:  订单编号，同步报单接口返回的编号
        :return: 返回订单编号对应的委托对象
        """
        req = XTQC.QueryStockOrdersReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_nOrderID = order_id
        
        seq = self.async_client.nextSeq()
        resp = self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStockOrdersWithSeq, seq, req)
        )
        if resp and len(resp):
            return resp[0]
        return None

    def query_stock_orders(self, account, cancelable_only = False):
        """
        :param account: 证券账号
        :param cancelable_only: 仅查询可撤委托
        :return: 返回当日所有委托的委托对象组成的list
        """
        req = XTQC.QueryStockOrdersReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_bCanCancel = cancelable_only
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStockOrdersWithSeq, seq, req)
        )
    
    def query_stock_orders_async(self, account, callback, cancelable_only = False):
        """
        :param account: 证券账号
        :param cancelable_only: 仅查询可撤委托
        :return: 返回当日所有委托的委托对象组成的list
        """
        req = XTQC.QueryStockOrdersReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_bCanCancel = cancelable_only
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryStockOrdersWithSeq, seq, req)
            , callback
        )
    
    def query_stock_trades(self, account):
        """
        :param account:  证券账号
        :return:  返回当日所有成交的成交对象组成的list
        """
        req = XTQC.QueryStockTradesReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStockTradesWithSeq, seq, req)
        )
    
    def query_stock_trades_async(self, account, callback):
        """
        :param account:  证券账号
        :return:  返回当日所有成交的成交对象组成的list
        """
        req = XTQC.QueryStockTradesReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryStockTradesWithSeq, seq, req)
            , callback
        )

    def query_stock_position(self, account, stock_code):
        """
        :param account: 证券账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :return: 返回证券代码对应的持仓对象
        """
        req = XTQC.QueryStockPositionsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        req.m_strStockCode = stock_code
        
        seq = self.async_client.nextSeq()
        resp = self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStockPositionsWithSeq, seq, req)
        )
        if resp and len(resp):
            return resp[0]
        return None

    def query_stock_positions(self, account):
        """
        :param account: 证券账号
        :return: 返回当日所有持仓的持仓对象组成的list
        """
        req = XTQC.QueryStockPositionsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStockPositionsWithSeq, seq, req)
        )
    
    def query_stock_positions_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回当日所有持仓的持仓对象组成的list
        """
        req = XTQC.QueryStockPositionsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq
            , (self.async_client.queryStockPositionsWithSeq, seq, req)
            , callback
        )

    def query_credit_detail(self, account):
        """
        :param account: 证券账号
        :return: 返回当前证券账号的资产数据
        """
        req = XTQC.QueryCreditDetailReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryCreditDetailWithSeq, seq, req)
        )
    
    def query_credit_detail_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回当前证券账号的资产数据
        """
        req = XTQC.QueryCreditDetailReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryCreditDetailWithSeq, seq, req)
            , callback
        )

    def query_stk_compacts(self, account):
        """
        :param account: 证券账号
        :return: 返回负债合约
        """
        req = XTQC.QueryStkCompactsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryStkCompactsWithSeq, seq, req)
        )
    
    def query_stk_compacts_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回负债合约
        """
        req = XTQC.QueryStkCompactsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryStkCompactsWithSeq, seq, req)
            , callback
        )
    
    def query_credit_subjects(self, account):
        """
        :param account: 证券账号
        :return: 返回融资融券标的
        """
        req = XTQC.QueryCreditSubjectsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryCreditSubjectsWithSeq, seq, req)
        )
    
    def query_credit_subjects_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回融资融券标的
        """
        req = XTQC.QueryCreditSubjectsReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryCreditSubjectsWithSeq, seq, req)
            , callback
        )
    
    def query_credit_slo_code(self, account):
        """
        :param account: 证券账号
        :return: 返回可融券数据
        """
        req = XTQC.QueryCreditSloCodeReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryCreditSloCodeWithSeq, seq, req)
        )
    
    def query_credit_slo_code_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回可融券数据
        """
        req = XTQC.QueryCreditSloCodeReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryCreditSloCodeWithSeq, seq, req)
            , callback
        )
    
    def query_credit_assure(self, account):
        """
        :param account: 证券账号
        :return: 返回标的担保品
        """
        req = XTQC.QueryCreditAssureReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryCreditAssureWithSeq, seq, req)
        )
    
    def query_credit_assure_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回标的担保品
        """
        req = XTQC.QueryCreditAssureReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryCreditAssureWithSeq, seq, req)
            , callback
        )
    
    def query_new_purchase_limit(self, account):
        """
        :param account: 证券账号
        :return: 返回账户新股申购额度数据
        """
        req = XTQC.QueryNewPurchaseLimitReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        new_purchase_limit_list = self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryNewPurchaseLimitWithSeq, seq, req)
        )
        new_purchase_limit_result = dict()
        for item in new_purchase_limit_list:
            new_purchase_limit_result[item.m_strNewPurchaseLimitKey] = item.m_nNewPurchaseLimitValue
        return new_purchase_limit_result
        
    def query_new_purchase_limit_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回账户新股申购额度数据
        """
        req = XTQC.QueryNewPurchaseLimitReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryNewPurchaseLimitWithSeq, seq, req)
            , callback
        )
    
    def query_ipo_data(self):
        """
        :return: 返回新股新债信息
        """
        req = XTQC.QueryIPODataReq()
        req.m_strIPOType = ''
        
        seq = self.async_client.nextSeq()
        ipo_data_list = self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryIPODataWithSeq, seq, req)
        )
        ipo_data_result = dict()
        for item in ipo_data_list:
            ipo_data_result[item.m_strIPOCode] = {
                'name': item.m_strIPOName, 
                'type':  item.m_strIPOType, 
                'maxPurchaseNum':  item.m_nMaxPurchaseNum, 
                'minPurchaseNum':  item.m_nMinPurchaseNum, 
                'purchaseDate':  item.m_strPurchaseDate, 
                'issuePrice': item.m_dIssuePrice,
            }
        return ipo_data_result
        
    def query_ipo_data_async(self, callback):
        """
        :return: 返回新股新债信息
        """
        req = XTQC.QueryIPODataReq()
        req.m_strIPOType = ''
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryIPODataWithSeq, seq, req)
            , callback
        )
    
    def query_appointment_info(self, account):
        """
        :param account: 证券账号
        :return: 返回约券合约信息
        """
        req = XTQC.QueryAppointmentInfoReq()
        req.m_nAccountType = 3
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        appointment_info_list = self.common_op_sync_with_seq(
            seq,
            (self.async_client.queryAppointmentInfoWithSeq, seq, req)
        )      
        appointment_info_result = dict()
        for item in appointment_info_list:
            appointment_info_result[item.m_strCompactId] = {
                'success': item.m_bSuccess,
                'error': item.m_strError,
                'fundAccount': item.m_strFundAccount,
                'origCompactId': item.m_strOrigCompactId,
                'exchangeType': item.m_strExchangeType,
                'stockCode': item.m_strStockCode,
                'stockName': item.m_strStockName,
                'contractEndDate': item.m_nContractEndDate,
                'feeRatio': item.m_dFeeRatio,
                'compactTerm': item.m_nCompactTerm,
                'compactAmount': item.m_nCompactAmount,
                'compactRepayDate': item.m_nCompactRepayDate,
                'compactStatus': item.m_strCompactStatus,
                'positionStr': item.m_strPositionStr,
            }
        return appointment_info_result
    
    def query_appointment_info_async(self, account, callback):
        """
        :param account: 证券账号
        :return: 返回约券合约信息
        """
        req = XTQC.QueryAppointmentInfoReq()
        req.m_nAccountType = account.account_type
        req.m_strAccountID = account.account_id
        
        seq = self.async_client.nextSeq()
        return self.common_op_async_with_seq(
            seq,
            (self.async_client.queryAppointmentInfoWithSeq, seq, req)
            , callback
        )

    def smt_appointment_async(self, account, stock_code, apt_days, apt_volume, fare_ratio, sub_rare_ratio, fine_ratio,
                          begin_date):
        """
        :param account: 证券账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param apt_days: 约定期限
        :param apt_volume: 约定数量
        :param fare_ratio: 约券费率
        :param sub_rare_ratio: 提前归还费率
        :param fine_ratio: 违约金率
        :param begin_date: 约定日期
        :return: 返回下单请求序号
        """
        req = XTQC.SmtAppointmentReq()
        req.m_strAccountID = account.account_id
        req.m_strStockCode = stock_code
        req.m_nAptDays = apt_days
        req.m_nVolume = apt_volume
        req.m_dFareRatio = fare_ratio
        req.m_dSubRareRatio = sub_rare_ratio
        req.m_dFineRatio = fine_ratio
        req.m_strBeginDate = begin_date
        
        
        seq = self.async_client.nextSeq()
        self.cbs[seq] = self.callback.on_smt_appointment_async_response
        self.async_client.smtAppointmentWithSeq(seq, req)
        return seq
       
    def query_smt_secu_info(self, account):
        """
        :param account: 证券账号
        :return: 返回券源券单信息
        """
        req = XTQC.QuerySMTSecuInfoReq()
        req.m_nAccountType = 3
        req.m_strAccountID = account.account_id

        seq = self.async_client.nextSeq()
        smt_secu_info_list = self.common_op_sync_with_seq(
            seq,
            (self.async_client.querySMTSecuInfoWithSeq, seq, req)
        )
        smt_secu_info_result = dict()
        for item in smt_secu_info_list:
            stock = item.m_strStockCode + '.' +item.m_strExchangeType
            smt_secu_info_result[stock] = {
                'success': item.m_bSuccess, 
                'error':  item.m_strError, 
                'stockName': item.m_strStockName,
                'creditType':  item.m_strCreditType, 
                'tradeType': item.m_strTradeType,
                'compactTerm': item.m_nCompactTerm,
                'maxTerm': item.m_nMaxTerm,
                'lendAmount': item.m_nLendAmount,
                'remark': item.m_strRemark,
                'fareWay': item.m_strFareWay,
                'fareRateNew': item.m_dFareRateNew,
            }
        return smt_secu_info_result
    
    def query_smt_secu_rate(self, account, stock_code, max_term, fare_way, credit_type, trade_type):
        """
        :param account: 证券账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param max_term: 最大约定期限
        :param fare_way: 折扣标志
        :param credit_type: 资券类型
        :param trade_type: 业务类型
        :return: 返回券源费率信息
        """
        req = XTQC.QuerySMTSecuRateReq()
        req.m_nAccountType = 3
        req.m_strAccountID = account.account_id
        req.m_strStockCode = stock_code
        req.m_nMaxTerm = max_term
        req.m_strFareWay = fare_way
        req.m_strCreditType = credit_type
        req.m_strTradeType = trade_type
        
        seq = self.async_client.nextSeq()
        smt_secu_rate_list = self.common_op_sync_with_seq(
            seq,
            (self.async_client.querySMTSecuRateWithSeq, seq, req)
        )
        smt_secu_rate_result = dict()
        if smt_secu_rate_list:
            item = smt_secu_rate_list[0]
            smt_secu_rate_result = {
                'success': item.m_bSuccess, 
                'error':  item.m_strError, 
                'fareRatio': item.m_dFareRatio,
                'subRareRatio': item.m_dSubRareRatio,
                'fineRatio': item.m_dFineRatio,
        }
        return smt_secu_rate_result