pip install grpcio grpcio-tools

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. .\qmt.proto 

python qmtServer.py

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