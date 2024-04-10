from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant import xtconstant
from xtquant import xtdata
import time
import qmtData

def order_buy(xt_trader,account,code,amount,price=0,strategy="Finhack-QMT",remark="autoBuy"):

    if int(price)==9999:
        info=qmtData.get_daily_info(code)
        lastprice=info['close']
        price=info['up_limit']
        if lastprice*1.02<up_limit:
            price=round(lastprice*1.02,2)
        else:
            price=round(up_limit,2)
        seq=xt_trader.order_stock_async(account, code, xtconstant.STOCK_BUY, amount, xtconstant.FIX_PRICE, price, strategy, remark)
    elif price>0:
        seq=xt_trader.order_stock_async(account, code, xtconstant.STOCK_BUY, amount, xtconstant.FIX_PRICE, price, strategy, remark)
    else:
        seq=xt_trader.order_stock_async(account, code, xtconstant.STOCK_BUY, amount, xtconstant.LATEST_PRICE, price, strategy, remark)
    print(f"下单买入{code}共计{amount}股，挂单价{price}")
    return seq


def order_sell(xt_trader,account,code,amount,price=0,strategy="Finhack-QMT",remark="autoSell"):
    if int(price)==-1:
        info=qmtData.get_daily_info(code)
        lastprice=info['close']
        down_limit=info['down_limit']
        if lastprice*0.98>down_limit:
            price=round(lastprice*0.98,2)
        else:
            price=round(down_limit,2)
        seq=xt_trader.order_stock_async(account, code, xtconstant.STOCK_SELL, amount, xtconstant.FIX_PRICE, price, strategy, remark)
    elif price>0:
        seq=xt_trader.order_stock_async(account, code, xtconstant.STOCK_SELL, amount, xtconstant.FIX_PRICE, price, strategy, remark)
    else:
        seq=xt_trader.order_stock_async(account, code, xtconstant.STOCK_SELL, amount, xtconstant.LATEST_PRICE, price, strategy,remark)
    print(f"下单卖出{code}共计{amount}股，挂单价{price}")
    return seq

def query_orders(xt_trader,account):
    o_tmp = xt_trader.query_stock_orders(account, False)
    orders=[]
    for o in o_tmp:
        orders.append({
            "stock_code":o.stock_code,
            "order_id":o.order_id,
            "order_sysid":o.order_sysid,
            "order_time":o.order_time,
            "order_type":o.order_type,
            "order_volume":o.order_volume,
            "price_type":o.price_type,
            "price":o.price,
            "traded_volume":o.traded_volume,
            "traded_price":o.traded_price,
            "order_status":o.order_status,
            "status_msg":o.status_msg,
            "strategy_name":o.strategy_name,
            "order_remark":o.order_remark,
            #"direction":o.direction,
            #"offset_flag":o.offset_flag
        })
    print("正在查询订单")
    print(orders)
    return orders


def cancel_orders(xt_trader,account):
    print("取消订单")
    orders=query_orders(xt_trader,account)
    for order in orders:
        print(order)
        if order['order_status'] not in [53,54,56,57,255]:
            xt_trader.cancel_order_stock_async(account, order['order_id'])
    pass


def retry_orders(xt_trader,account):
    print("重新挂单")
    orders=query_orders(xt_trader,account)
    for order in orders:
        if order['order_status'] not in [53,54,56,57,255]:
            print(order)

            xt_trader.cancel_order_stock_async(account, order['order_id'])
            time.sleep(1)
            xt_trader.order_stock_async(account,order['stock_code'], order['order_type'], order['order_volume']-order['traded_volume'], xtconstant.LATEST_PRICE, order['price'], order['strategy_name'],order['order_remark'])
    pass


# 委托状态(order_status)
# 枚举变量名	值	含义
# xtconstant.ORDER_UNREPORTED	48	未报
# xtconstant.ORDER_WAIT_REPORTING	49	待报
# xtconstant.ORDER_REPORTED	50	已报
# xtconstant.ORDER_REPORTED_CANCEL	51	已报待撤
# xtconstant.ORDER_PARTSUCC_CANCEL	52	部成待撤
# xtconstant.ORDER_PART_CANCEL	53	部撤
# xtconstant.ORDER_CANCELED	54	已撤
# xtconstant.ORDER_PART_SUCC	55	部成
# xtconstant.ORDER_SUCCEEDED	56	已成
# xtconstant.ORDER_JUNK	57	废单
# xtconstant.ORDER_UNKNOWN	255	未知
