# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import qmt_pb2 as qmt__pb2


class QmtServiceStub(object):
    """定义服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetPrice = channel.unary_unary(
                '/qmt.QmtService/GetPrice',
                request_serializer=qmt__pb2.PriceRequest.SerializeToString,
                response_deserializer=qmt__pb2.PriceResponse.FromString,
                )
        self.GetDailyInfo = channel.unary_unary(
                '/qmt.QmtService/GetDailyInfo',
                request_serializer=qmt__pb2.DailyInfoRequest.SerializeToString,
                response_deserializer=qmt__pb2.DailyInfoResponse.FromString,
                )
        self.OrderBuy = channel.unary_unary(
                '/qmt.QmtService/OrderBuy',
                request_serializer=qmt__pb2.OrderRequest.SerializeToString,
                response_deserializer=qmt__pb2.OrderResponse.FromString,
                )
        self.OrderSell = channel.unary_unary(
                '/qmt.QmtService/OrderSell',
                request_serializer=qmt__pb2.OrderRequest.SerializeToString,
                response_deserializer=qmt__pb2.OrderResponse.FromString,
                )
        self.QueryOrders = channel.unary_unary(
                '/qmt.QmtService/QueryOrders',
                request_serializer=qmt__pb2.QueryOrdersRequest.SerializeToString,
                response_deserializer=qmt__pb2.OrdersResponse.FromString,
                )
        self.CancelOrders = channel.unary_unary(
                '/qmt.QmtService/CancelOrders',
                request_serializer=qmt__pb2.QueryOrdersRequest.SerializeToString,
                response_deserializer=qmt__pb2.OrdersResponse.FromString,
                )
        self.RetryOrders = channel.unary_unary(
                '/qmt.QmtService/RetryOrders',
                request_serializer=qmt__pb2.QueryOrdersRequest.SerializeToString,
                response_deserializer=qmt__pb2.OrdersResponse.FromString,
                )
        self.GetAsset = channel.unary_unary(
                '/qmt.QmtService/GetAsset',
                request_serializer=qmt__pb2.AssetRequest.SerializeToString,
                response_deserializer=qmt__pb2.AssetResponse.FromString,
                )
        self.GetPositions = channel.unary_unary(
                '/qmt.QmtService/GetPositions',
                request_serializer=qmt__pb2.AssetRequest.SerializeToString,
                response_deserializer=qmt__pb2.PositionsResponse.FromString,
                )


class QmtServiceServicer(object):
    """定义服务
    """

    def GetPrice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDailyInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OrderBuy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OrderSell(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryOrders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelOrders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetryOrders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAsset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPositions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QmtServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetPrice': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPrice,
                    request_deserializer=qmt__pb2.PriceRequest.FromString,
                    response_serializer=qmt__pb2.PriceResponse.SerializeToString,
            ),
            'GetDailyInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDailyInfo,
                    request_deserializer=qmt__pb2.DailyInfoRequest.FromString,
                    response_serializer=qmt__pb2.DailyInfoResponse.SerializeToString,
            ),
            'OrderBuy': grpc.unary_unary_rpc_method_handler(
                    servicer.OrderBuy,
                    request_deserializer=qmt__pb2.OrderRequest.FromString,
                    response_serializer=qmt__pb2.OrderResponse.SerializeToString,
            ),
            'OrderSell': grpc.unary_unary_rpc_method_handler(
                    servicer.OrderSell,
                    request_deserializer=qmt__pb2.OrderRequest.FromString,
                    response_serializer=qmt__pb2.OrderResponse.SerializeToString,
            ),
            'QueryOrders': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryOrders,
                    request_deserializer=qmt__pb2.QueryOrdersRequest.FromString,
                    response_serializer=qmt__pb2.OrdersResponse.SerializeToString,
            ),
            'CancelOrders': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelOrders,
                    request_deserializer=qmt__pb2.QueryOrdersRequest.FromString,
                    response_serializer=qmt__pb2.OrdersResponse.SerializeToString,
            ),
            'RetryOrders': grpc.unary_unary_rpc_method_handler(
                    servicer.RetryOrders,
                    request_deserializer=qmt__pb2.QueryOrdersRequest.FromString,
                    response_serializer=qmt__pb2.OrdersResponse.SerializeToString,
            ),
            'GetAsset': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAsset,
                    request_deserializer=qmt__pb2.AssetRequest.FromString,
                    response_serializer=qmt__pb2.AssetResponse.SerializeToString,
            ),
            'GetPositions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPositions,
                    request_deserializer=qmt__pb2.AssetRequest.FromString,
                    response_serializer=qmt__pb2.PositionsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'qmt.QmtService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QmtService(object):
    """定义服务
    """

    @staticmethod
    def GetPrice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/GetPrice',
            qmt__pb2.PriceRequest.SerializeToString,
            qmt__pb2.PriceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDailyInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/GetDailyInfo',
            qmt__pb2.DailyInfoRequest.SerializeToString,
            qmt__pb2.DailyInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OrderBuy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/OrderBuy',
            qmt__pb2.OrderRequest.SerializeToString,
            qmt__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def OrderSell(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/OrderSell',
            qmt__pb2.OrderRequest.SerializeToString,
            qmt__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/QueryOrders',
            qmt__pb2.QueryOrdersRequest.SerializeToString,
            qmt__pb2.OrdersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/CancelOrders',
            qmt__pb2.QueryOrdersRequest.SerializeToString,
            qmt__pb2.OrdersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetryOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/RetryOrders',
            qmt__pb2.QueryOrdersRequest.SerializeToString,
            qmt__pb2.OrdersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAsset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/GetAsset',
            qmt__pb2.AssetRequest.SerializeToString,
            qmt__pb2.AssetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPositions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/qmt.QmtService/GetPositions',
            qmt__pb2.AssetRequest.SerializeToString,
            qmt__pb2.PositionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
