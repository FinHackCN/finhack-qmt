# qmt_server.py
from concurrent import futures
import grpc
import qmt_pb2
import qmt_pb2_grpc
import qmtAccount
import qmtTrader
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from xtquant import xtdata
import requests
from datetime import datetime, timedelta
import json
import random
import qmtData
import qmtCallback
import time
import config

class QmtServiceServicer(qmt_pb2_grpc.QmtServiceServicer):
    def __init__(self):
        # path为mini qmt客户端安装目录下userdata_mini路径
        path = config.path
        # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
        session_id = random.randint(0,9999999999)
        xt_trader = XtQuantTrader(path, session_id)
        account = StockAccount(config.account_id,config.account_type)
        callback = qmtCallback.MyXtQuantTraderCallback()
        xt_trader.register_callback(callback)
        # 启动交易线程
        xt_trader.start()
        # 建立交易连接，返回0表示连接成功
        connect_result = xt_trader.connect()
        if connect_result != 0:
            print(connect_result)
            import sys
            sys.exit('链接失败，程序即将退出 %d'%connect_result)
        self.xt_trader=xt_trader
        self.account=account



    def GetPrice(self, request, context):
        code=request.code
        price=qmtData.get_price(code)
        return qmt_pb2.PriceResponse(last_price=price)

    def GetDailyInfo(self, request, context):
        code=request.code
        info=qmtData.get_daily_info(code)
        return qmt_pb2.DailyInfoResponse(**info)

    def OrderBuy(self, request, context):
        code=request.code
        amount=request.amount
        price=request.price
        seq=qmtTrader.order_buy(xt_trader=self.xt_trader,account=self.account,code=code,amount=amount,price=price)
        return qmt_pb2.OrderResponse(seq=seq)

    def OrderSell(self, request, context):
        code=request.code
        amount=request.amount
        price=request.price
        seq=qmtTrader.order_sell(xt_trader=self.xt_trader,account=self.account,code=code,amount=amount,price=price)
        return qmt_pb2.OrderResponse(seq=seq)

    def QueryOrders(self, request, context):
        orders=qmtTrader.query_orders(self.xt_trader,self.account)
        return qmt_pb2.OrdersResponse(orders=orders)

    def CancelOrders(self, request, context):
        qmtTrader.cancel_orders(self.xt_trader,self.account)
        return qmt_pb2.OrdersResponse()

    def RetryOrders(self, request, context):
        qmtTrader.retry_orders(self.xt_trader,self.account)
        return qmt_pb2.OrdersResponse()

    def GetAsset(self, request, context):
        asset=qmtAccount.get_asset(self.xt_trader,self.account)
        return qmt_pb2.AssetResponse(**asset)

    def GetPositions(self, request, context):
        positions=qmtAccount.get_positions(self.xt_trader,self.account)
        return qmt_pb2.PositionsResponse(positions=positions)




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    qmt_pb2_grpc.add_QmtServiceServicer_to_server(QmtServiceServicer(), server)
    server.add_insecure_port(config.server)
    server.start()
    print(f"服务已启动！正在监听{config.server}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()