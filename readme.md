由于finhack框架是Linux下的，而QMT是运行在Windows下的，因此这两个之间需要进行通信，所以封装了一个适合低频策略的简单的QMT接口，主要就是实现了持仓查询和买卖接口。

具体都需要啥依赖自己看着装吧，缺啥装啥，然后由于通信是使用grpc，因此必须安装下面这俩

    pip install grpcio grpcio-tools

里面的qmt_pb2和qmt_pb2_grpc是通过grpc_tools生成的，不同版本可能会有问题，因此建议装完grpc_tools重新使用下面命令生成一下

    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. .\qmt.proto 

在config.py里配置好QMT的路径，以及资金账号，运行 python qmtServer.py 启动服务，其它机器使用qmtClient调用

    from qmtClient import qclient
    
    print('------------------------')
    asset=qclient.getAsset()
    print(asset)
    price=qclient.getPrice("002624.SZ")
    print(price)
    info=qclient.getInfo("002624.SZ")
    print(info)

    seq=qclient.OrderBuy(code="002624.SZ",amount=100,price=11)#限价买入
    seq=qclient.OrderBuy(code="002624.SZ",amount=100)#市价买入
    seq=qclient.RetryOrders()
    seq=qclient.CancelOrders()

    seq=qclient.OrderSell(code="002624.SZ",amount=100,price=13)#限价卖出
    seq=qclient.OrderSell(code="002624.SZ",amount=100)#市价卖出
    seq=qclient.CancelOrders()
    seq=qclient.RetryOrders()

    orders=qclient.GetPositions()
    print(orders)

    positions=qclient.GetPositions()
    print(positions)

![image](https://github.com/FinHackCN/finhack-qmt/assets/6196607/89c2cbc1-3a77-40e1-8e6e-b51e6c284b68)
