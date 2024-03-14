#coding=utf-8
from . import xtconstant

"""
定义Python的数据结构,给Python策略使用
包含股票+信用
"""

class StockAccount(object):
    """
    定义证券账号类, 用于证券账号的报撤单等
    """
    def __new__(cls, account_id, account_type = 'STOCK'):
        """
        :param account_id: 资金账号
        :return: 若资金账号不为字符串，返回类型错误
        """
        if not isinstance(account_id, str):
            return u"资金账号必须为字符串类型"
        return super(StockAccount, cls).__new__(cls)

    def __init__(self, account_id, account_type = 'STOCK'):
        """
        :param account_id: 资金账号
        """
        account_type = account_type.upper()
        if(account_type == "STOCK"):
            self.account_type = xtconstant.SECURITY_ACCOUNT
        elif(account_type == "CREDIT"):
            self.account_type = xtconstant.CREDIT_ACCOUNT
        elif(account_type == "FUTURE"):
            self.account_type = xtconstant.FUTURE_ACCOUNT
        elif(account_type == "HUGANGTONG"):
            self.account_type = xtconstant.HUGANGTONG_ACCOUNT
        elif(account_type == "SHENGANGTONG"):
            self.account_type = xtconstant.SHENGANGTONG_ACCOUNT
        else:
            self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id


class XtAsset(object):
    """
    迅投股票账号资金结构
    """
    def __init__(self, account_id, cash, frozen_cash, market_value, total_asset):
        """
        :param account_id: 资金账号
        :param cash: 可用
        :param frozen_cash: 冻结
        :param market_value: 持仓市值
        :param total_asset: 总资产
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.cash = cash
        self.frozen_cash = frozen_cash
        self.market_value = market_value
        self.total_asset = total_asset


class XtOrder(object):
    """
    迅投股票委托结构
    """
    def __init__(self, account_id, stock_code,
                 order_id, order_sysid, order_time, order_type, order_volume,
                 price_type, price, traded_volume, traded_price,
                 order_status, status_msg, strategy_name, order_remark):
        """
        :param account_id: 资金账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param order_id: 委托编号
        :param order_sysid: 柜台编号
        :param order_time: 报单时间
        :param order_type: 委托类型, 23:买, 24:卖
        :param order_volume: 委托数量, 股票以'股'为单位, 债券以'张'为单位
        :param price_type: 报价类型, 详见帮助手册
        :param price: 报价价格，如果price_type为指定价, 那price为指定的价格，否则填0
        :param traded_volume: 成交数量, 股票以'股'为单位, 债券以'张'为单位
        :param traded_price: 成交均价
        :param order_status: 委托状态
        :param status_msg: 委托状态描述, 如废单原因
        :param strategy_name: 策略名称
        :param order_remark: 委托备注
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.stock_code = stock_code
        self.order_id = order_id
        self.order_sysid = order_sysid
        self.order_time = order_time
        self.order_type = order_type
        self.order_volume = order_volume
        self.price_type = price_type
        self.price = price
        self.traded_volume = traded_volume
        self.traded_price = traded_price
        self.order_status = order_status
        self.status_msg = status_msg
        self.strategy_name = strategy_name
        self.order_remark = order_remark


class XtTrade(object):
    """
    迅投股票成交结构
    """
    def __init__(self, account_id, stock_code,
                 order_type, traded_id, traded_time, traded_price, traded_volume, traded_amount,
                 order_id, order_sysid, strategy_name, order_remark):
        """
        :param account_id: 资金账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param order_type: 委托类型
        :param traded_id: 成交编号
        :param traded_time: 成交时间
        :param traded_price: 成交均价
        :param traded_volume: 成交数量, 股票以'股'为单位, 债券以'张'为单位
        :param traded_amount: 成交金额
        :param order_id: 委托编号
        :param order_sysid: 柜台编号
        :param strategy_name: 策略名称
        :param order_remark: 委托备注
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.order_type = order_type
        self.stock_code = stock_code
        self.traded_id = traded_id
        self.traded_time = traded_time
        self.traded_price = traded_price
        self.traded_volume = traded_volume
        self.traded_amount = traded_amount
        self.order_id = order_id
        self.order_sysid = order_sysid
        self.strategy_name = strategy_name
        self.order_remark = order_remark


class XtPosition(object):
    """
    迅投股票持仓结构
    """
    def __init__(self, account_id, stock_code,
                 volume, can_use_volume, open_price, market_value,
                 frozen_volume, on_road_volume, yesterday_volume):
        """
        :param account_id: 资金账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param volume: 持仓数量,股票以'股'为单位, 债券以'张'为单位
        :param can_use_volume: 可用数量, 股票以'股'为单位, 债券以'张'为单位
        :param open_price: 平均建仓成本
        :param market_value: 市值
        :param frozen_volume: 冻结数量
        :param on_road_volume: 在途股份
        :param yesterday_volume: 昨夜拥股
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.stock_code = stock_code
        self.volume = volume
        self.can_use_volume = can_use_volume
        self.open_price = open_price
        self.market_value = market_value
        self.frozen_volume = frozen_volume
        self.on_road_volume = on_road_volume
        self.yesterday_volume = yesterday_volume


class XtOrderError(object):
    """
    迅投股票委托失败结构
    """
    def __init__(self, account_id, order_id,
                 error_id=None, error_msg=None,
                 strategy_name=None, order_remark=None):
        """
        :param account_id: 资金账号
        :param order_id: 订单编号
        :param error_id: 报单失败错误码
        :param error_msg: 报单失败具体信息
        :param strategy_name: 策略名称
        :param order_remark: 委托备注
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.order_id = order_id
        self.error_id = error_id
        self.error_msg = error_msg
        self.strategy_name = strategy_name
        self.order_remark = order_remark


class XtCancelError(object):
    """
    迅投股票委托撤单失败结构
    """
    def __init__(self, account_id, order_id, market, order_sysid,
                 error_id=None, error_msg=None):
        """
        :param account_id: 资金账号
        :param order_id: 订单编号
        :param market: 交易市场 0:上海 1:深圳
        :param order_sysid: 柜台委托编号
        :param error_id: 撤单失败错误码
        :param error_msg: 撤单失败具体信息
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.order_id = order_id
        self.market = market
        self.order_sysid = order_sysid
        self.error_id = error_id
        self.error_msg = error_msg


class XtOrderResponse(object):
    """
    迅投异步下单接口对应的委托反馈
    """
    def __init__(self, account_id, order_id, strategy_name, order_remark, error_msg, seq):
        """
        :param account_id: 资金账号
        :param order_id: 订单编号
        :param strategy_name: 策略名称
        :param order_remark: 委托备注
        :param seq: 下单请求序号
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.order_id = order_id
        self.strategy_name = strategy_name
        self.order_remark = order_remark
        self.error_msg = error_msg
        self.seq = seq

class XtAppointmentResponse(object):
    """
    迅投异步约券接口对应的委托反馈 
    """
    def __init__(self, account_id, order_id, error_id, error_msg, seq):
        """
        :param account_id: 资金账号
        :param order_sysid: 订单编号
        :param error_id: 错误编号
        :param error_msg: 错误信息
        :param seq: 下单请求序号
        """
        if error_id == 0:
            self.order_sysid = error_msg
            self.error_msg = ''
        else:
            self.order_sysid = str(order_id)
            self.error_msg = error_msg
        
        self.account_id = account_id
        self.error_id = error_id
        self.seq = seq

class XtCancelOrderResponse(object):
    """
    迅投异步委托撤单请求返回结构
    """
    def __init__(self, account_id, cancel_result, order_id, order_sysid, seq):
        """
        :param account_id: 资金账号
        :param cancel_result: 撤单结果
        :param order_id: 订单编号
        :param order_sysid: 柜台委托编号
        :param seq: 撤单请求序号
        """
        self.account_type = xtconstant.SECURITY_ACCOUNT
        self.account_id = account_id
        self.cancel_result = cancel_result
        self.order_id = order_id
        self.order_sysid = order_sysid
        self.seq = seq


class XtCreditOrder(XtOrder):
    """
    迅投信用委托结构
    """
    def __init__(self, account_id, stock_code,
                 order_id, order_time, order_type, order_volume,
                 price_type, price, traded_volume, traded_price,
                 order_status, status_msg, order_remark, contract_no):
        """
        :param account_id: 资金账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param order_id: 委托编号
        :param order_time: 报单时间
        :param order_type: 委托类型, 23:买, 24:卖
        :param order_volume: 委托数量, 股票以'股'为单位, 债券以'张'为单位
        :param price_type: 报价类型, 详见帮助手册
        :param price: 报价价格，如果price_type为指定价, 那price为指定的价格，否则填0
        :param traded_volume: 成交数量, 股票以'股'为单位, 债券以'张'为单位
        :param traded_price: 成交均价
        :param order_status: 委托状态
        :param status_msg: 委托状态描述, 如废单原因
        :param order_remark: 委托备注
        :param contract_no: 两融合同编号
        """
        self.account_type = xtconstant.CREDIT_ACCOUNT
        self.account_id = account_id
        self.stock_code = stock_code
        self.order_id = order_id
        self.order_time = order_time
        self.order_type = order_type
        self.order_volume = order_volume
        self.price_type = price_type
        self.price = price
        self.traded_volume = traded_volume
        self.traded_price = traded_price
        self.order_status = order_status
        self.status_msg = status_msg
        self.order_remark = order_remark
        self.contract_no = contract_no


class XtCreditDeal(object):
    """
    迅投信用成交结构
    """
    def __init__(self, account_id, stock_code,
                 traded_id, traded_time, traded_price,
                 traded_volume, order_id, contract_no):
        """
        :param account_id: 资金账号
        :param stock_code: 证券代码, 例如"600000.SH"
        :param traded_id: 成交编号
        :param traded_time: 成交时间
        :param traded_price: 成交均价
        :param traded_volume: 成交数量, 股票以'股'为单位, 债券以'张'为单位
        :param order_id: 委托编号
        :param contract_no: 两融合同编号
        """
        self.account_type = xtconstant.CREDIT_ACCOUNT
        self.account_id = account_id
        self.stock_code = stock_code
        self.traded_id = traded_id
        self.traded_time = traded_time
        self.traded_price = traded_price
        self.traded_volume = traded_volume
        self.order_id = order_id
        self.contract_no = contract_no

class XtAccountStatus(object):
    """
    迅投账号状态结构
    """
    def __init__(self, account_id, account_type, status):
        """
        :param account_id: 资金账号
        :param account_type: 账号状态
        :param status: 账号状态，详细见账号状态定义
        """
        self.account_type = account_type
        self.account_id = account_id
        self.status = status