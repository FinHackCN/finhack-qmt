# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qmt.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tqmt.proto\x12\x03qmt\"\x1c\n\x0cPriceRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\"#\n\rPriceResponse\x12\x12\n\nlast_price\x18\x01 \x01(\x01\" \n\x10\x44\x61ilyInfoRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\"\xcc\x01\n\x11\x44\x61ilyInfoResponse\x12\x0f\n\x07ts_code\x18\x01 \x01(\t\x12\x0c\n\x04open\x18\x02 \x01(\x01\x12\x0c\n\x04high\x18\x03 \x01(\x01\x12\x0b\n\x03low\x18\x04 \x01(\x01\x12\r\n\x05\x63lose\x18\x05 \x01(\x01\x12\x0e\n\x06volume\x18\x06 \x01(\x01\x12\x0e\n\x06\x61mount\x18\x07 \x01(\x01\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x0c\n\x04vwap\x18\t \x01(\x01\x12\x0c\n\x04stop\x18\n \x01(\x05\x12\x10\n\x08up_limit\x18\x0b \x01(\x01\x12\x12\n\ndown_limit\x18\x0c \x01(\x01\"]\n\x0cOrderRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\x12\r\n\x05price\x18\x03 \x01(\x01\x12\x10\n\x08strategy\x18\x04 \x01(\t\x12\x0e\n\x06remark\x18\x05 \x01(\t\"\x1c\n\rOrderResponse\x12\x0b\n\x03seq\x18\x01 \x01(\x05\"\x14\n\x12QueryOrdersRequest\"\xad\x02\n\x0bOrderDetail\x12\x12\n\nstock_code\x18\x01 \x01(\t\x12\x10\n\x08order_id\x18\x02 \x01(\t\x12\x13\n\x0border_sysid\x18\x03 \x01(\t\x12\x12\n\norder_time\x18\x04 \x01(\t\x12\x12\n\norder_type\x18\x05 \x01(\x05\x12\x14\n\x0corder_volume\x18\x06 \x01(\x05\x12\x12\n\nprice_type\x18\x07 \x01(\x05\x12\r\n\x05price\x18\x08 \x01(\x01\x12\x15\n\rtraded_volume\x18\t \x01(\x05\x12\x14\n\x0ctraded_price\x18\n \x01(\x01\x12\x14\n\x0corder_status\x18\x0b \x01(\x05\x12\x12\n\nstatus_msg\x18\x0c \x01(\t\x12\x15\n\rstrategy_name\x18\r \x01(\t\x12\x14\n\x0corder_remark\x18\x0e \x01(\t\"2\n\x0eOrdersResponse\x12 \n\x06orders\x18\x01 \x03(\x0b\x32\x10.qmt.OrderDetail\"\x0e\n\x0c\x41ssetRequest\"k\n\rAssetResponse\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x0c\n\x04\x63\x61sh\x18\x02 \x01(\x01\x12\x13\n\x0b\x66rozen_cash\x18\x03 \x01(\x01\x12\x14\n\x0cmarket_value\x18\x04 \x01(\x01\x12\x13\n\x0btotal_value\x18\x05 \x01(\x01\";\n\x11PositionsResponse\x12&\n\tpositions\x18\x01 \x03(\x0b\x32\x13.qmt.PositionDetail\"\xa0\x01\n\x0ePositionDetail\x12\x12\n\nstock_code\x18\x01 \x01(\t\x12\x0e\n\x06volume\x18\x02 \x01(\x05\x12\x16\n\x0e\x63\x61n_use_volume\x18\x03 \x01(\x05\x12\x12\n\nopen_price\x18\x04 \x01(\x01\x12\x14\n\x0cmarket_value\x18\x05 \x01(\x01\x12\x15\n\rfrozen_volume\x18\x06 \x01(\x05\x12\x11\n\tavg_price\x18\x07 \x01(\x01\x32\x9d\x04\n\nQmtService\x12\x33\n\x08GetPrice\x12\x11.qmt.PriceRequest\x1a\x12.qmt.PriceResponse\"\x00\x12?\n\x0cGetDailyInfo\x12\x15.qmt.DailyInfoRequest\x1a\x16.qmt.DailyInfoResponse\"\x00\x12\x33\n\x08OrderBuy\x12\x11.qmt.OrderRequest\x1a\x12.qmt.OrderResponse\"\x00\x12\x34\n\tOrderSell\x12\x11.qmt.OrderRequest\x1a\x12.qmt.OrderResponse\"\x00\x12=\n\x0bQueryOrders\x12\x17.qmt.QueryOrdersRequest\x1a\x13.qmt.OrdersResponse\"\x00\x12>\n\x0c\x43\x61ncelOrders\x12\x17.qmt.QueryOrdersRequest\x1a\x13.qmt.OrdersResponse\"\x00\x12=\n\x0bRetryOrders\x12\x17.qmt.QueryOrdersRequest\x1a\x13.qmt.OrdersResponse\"\x00\x12\x33\n\x08GetAsset\x12\x11.qmt.AssetRequest\x1a\x12.qmt.AssetResponse\"\x00\x12;\n\x0cGetPositions\x12\x11.qmt.AssetRequest\x1a\x16.qmt.PositionsResponse\"\x00\x62\x06proto3')



_PRICEREQUEST = DESCRIPTOR.message_types_by_name['PriceRequest']
_PRICERESPONSE = DESCRIPTOR.message_types_by_name['PriceResponse']
_DAILYINFOREQUEST = DESCRIPTOR.message_types_by_name['DailyInfoRequest']
_DAILYINFORESPONSE = DESCRIPTOR.message_types_by_name['DailyInfoResponse']
_ORDERREQUEST = DESCRIPTOR.message_types_by_name['OrderRequest']
_ORDERRESPONSE = DESCRIPTOR.message_types_by_name['OrderResponse']
_QUERYORDERSREQUEST = DESCRIPTOR.message_types_by_name['QueryOrdersRequest']
_ORDERDETAIL = DESCRIPTOR.message_types_by_name['OrderDetail']
_ORDERSRESPONSE = DESCRIPTOR.message_types_by_name['OrdersResponse']
_ASSETREQUEST = DESCRIPTOR.message_types_by_name['AssetRequest']
_ASSETRESPONSE = DESCRIPTOR.message_types_by_name['AssetResponse']
_POSITIONSRESPONSE = DESCRIPTOR.message_types_by_name['PositionsResponse']
_POSITIONDETAIL = DESCRIPTOR.message_types_by_name['PositionDetail']
PriceRequest = _reflection.GeneratedProtocolMessageType('PriceRequest', (_message.Message,), {
  'DESCRIPTOR' : _PRICEREQUEST,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.PriceRequest)
  })
_sym_db.RegisterMessage(PriceRequest)

PriceResponse = _reflection.GeneratedProtocolMessageType('PriceResponse', (_message.Message,), {
  'DESCRIPTOR' : _PRICERESPONSE,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.PriceResponse)
  })
_sym_db.RegisterMessage(PriceResponse)

DailyInfoRequest = _reflection.GeneratedProtocolMessageType('DailyInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _DAILYINFOREQUEST,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.DailyInfoRequest)
  })
_sym_db.RegisterMessage(DailyInfoRequest)

DailyInfoResponse = _reflection.GeneratedProtocolMessageType('DailyInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _DAILYINFORESPONSE,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.DailyInfoResponse)
  })
_sym_db.RegisterMessage(DailyInfoResponse)

OrderRequest = _reflection.GeneratedProtocolMessageType('OrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _ORDERREQUEST,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.OrderRequest)
  })
_sym_db.RegisterMessage(OrderRequest)

OrderResponse = _reflection.GeneratedProtocolMessageType('OrderResponse', (_message.Message,), {
  'DESCRIPTOR' : _ORDERRESPONSE,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.OrderResponse)
  })
_sym_db.RegisterMessage(OrderResponse)

QueryOrdersRequest = _reflection.GeneratedProtocolMessageType('QueryOrdersRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYORDERSREQUEST,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.QueryOrdersRequest)
  })
_sym_db.RegisterMessage(QueryOrdersRequest)

OrderDetail = _reflection.GeneratedProtocolMessageType('OrderDetail', (_message.Message,), {
  'DESCRIPTOR' : _ORDERDETAIL,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.OrderDetail)
  })
_sym_db.RegisterMessage(OrderDetail)

OrdersResponse = _reflection.GeneratedProtocolMessageType('OrdersResponse', (_message.Message,), {
  'DESCRIPTOR' : _ORDERSRESPONSE,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.OrdersResponse)
  })
_sym_db.RegisterMessage(OrdersResponse)

AssetRequest = _reflection.GeneratedProtocolMessageType('AssetRequest', (_message.Message,), {
  'DESCRIPTOR' : _ASSETREQUEST,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.AssetRequest)
  })
_sym_db.RegisterMessage(AssetRequest)

AssetResponse = _reflection.GeneratedProtocolMessageType('AssetResponse', (_message.Message,), {
  'DESCRIPTOR' : _ASSETRESPONSE,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.AssetResponse)
  })
_sym_db.RegisterMessage(AssetResponse)

PositionsResponse = _reflection.GeneratedProtocolMessageType('PositionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _POSITIONSRESPONSE,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.PositionsResponse)
  })
_sym_db.RegisterMessage(PositionsResponse)

PositionDetail = _reflection.GeneratedProtocolMessageType('PositionDetail', (_message.Message,), {
  'DESCRIPTOR' : _POSITIONDETAIL,
  '__module__' : 'qmt_pb2'
  # @@protoc_insertion_point(class_scope:qmt.PositionDetail)
  })
_sym_db.RegisterMessage(PositionDetail)

_QMTSERVICE = DESCRIPTOR.services_by_name['QmtService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PRICEREQUEST._serialized_start=18
  _PRICEREQUEST._serialized_end=46
  _PRICERESPONSE._serialized_start=48
  _PRICERESPONSE._serialized_end=83
  _DAILYINFOREQUEST._serialized_start=85
  _DAILYINFOREQUEST._serialized_end=117
  _DAILYINFORESPONSE._serialized_start=120
  _DAILYINFORESPONSE._serialized_end=324
  _ORDERREQUEST._serialized_start=326
  _ORDERREQUEST._serialized_end=419
  _ORDERRESPONSE._serialized_start=421
  _ORDERRESPONSE._serialized_end=449
  _QUERYORDERSREQUEST._serialized_start=451
  _QUERYORDERSREQUEST._serialized_end=471
  _ORDERDETAIL._serialized_start=474
  _ORDERDETAIL._serialized_end=775
  _ORDERSRESPONSE._serialized_start=777
  _ORDERSRESPONSE._serialized_end=827
  _ASSETREQUEST._serialized_start=829
  _ASSETREQUEST._serialized_end=843
  _ASSETRESPONSE._serialized_start=845
  _ASSETRESPONSE._serialized_end=952
  _POSITIONSRESPONSE._serialized_start=954
  _POSITIONSRESPONSE._serialized_end=1013
  _POSITIONDETAIL._serialized_start=1016
  _POSITIONDETAIL._serialized_end=1176
  _QMTSERVICE._serialized_start=1179
  _QMTSERVICE._serialized_end=1720
# @@protoc_insertion_point(module_scope)
