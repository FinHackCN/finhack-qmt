from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
from xtquant import xtdata

def get_asset(xt_trader,account):
    print(f"正在查询资产信息")
    asset_tmp=xt_trader.query_stock_asset(account)
    asset={
        "user":asset_tmp.account_id,
        "cash":asset_tmp.cash,
        "frozen_cash":asset_tmp.frozen_cash,
        "market_value":asset_tmp.market_value,
        "total_value":asset_tmp.total_asset
    }
    print(asset)
    return asset

def get_positions(xt_trader,account):
    print(f"正在查询持仓信息")
    p_tmp=xt_trader.query_stock_positions(account)
    positions=[]
    for pos in p_tmp:
          positions.append({
               "stock_code":pos.stock_code,
               "volume":pos.volume,
               "can_use_volume":pos.can_use_volume,
               "open_price":pos.open_price,
               "market_value":pos.market_value,
               "frozen_volume":pos.frozen_volume,
               "avg_price":pos.open_price
          })
    print(positions)
    return positions
