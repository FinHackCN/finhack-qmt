#coding:utf-8

import os, sys
import datetime as dt
import traceback
import json

from . import xtbson as bson

from .IPythonApiClient import IPythonApiClient as RPCClient

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0} raise {1}:{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            # raise exc_type(message)
            print(message)
            return None

    return wrapper


CLIENT = None

from os.path import abspath, dirname
__curdir = dirname(abspath(__file__))

__rpc_config = __curdir + '/xtdata.ini'
__xtdata_config = __curdir + '/xtdata.ini'

from .IPythonApiClient import rpc_init
__rpc_init_status = rpc_init(__rpc_config)
if __rpc_init_status < 0:
    print(f'rpc初始化失败，配置文件：{__rpc_config}')

def get_client():
    global CLIENT
    if not CLIENT:
        CLIENT = RPCClient('client_xtdata', __xtdata_config)

        try:
            CLIENT.load_config(__xtdata_config)
            config = json.load(open(os.path.join('..', 'config', 'xtquantconfig.json')))
            port = config['port']
            CLIENT.set_remote_addr('localhost', port)
            CLIENT.reset()
            CLIENT.connect_ex()
        except Exception as e:
            pass

        if not CLIENT.is_connected():
            CLIENT.load_config(__xtdata_config)
            CLIENT.reset()

    if not CLIENT.is_connected():
        succ, errmsg = CLIENT.connect_ex()
        if not succ:
            raise Exception("无法连接服务！")
    return CLIENT


def reconnect(ip = 'localhost', port = 58610):
    global CLIENT
    CLIENT = None
    if not CLIENT:
        CLIENT = RPCClient('client_xtdata', __xtdata_config)

        CLIENT.load_config(__xtdata_config)
        CLIENT.set_remote_addr(ip, port)
        CLIENT.reset()
        CLIENT.connect()

    if not CLIENT.is_connected():
        if not CLIENT.connect():
            raise Exception("无法连接服务！")
    return

def create_view(viewID, view_type, title, group_id):
    client = get_client()
    return client.createView(viewID, view_type, title, group_id)

#def reset_view(viewID):
#    return

def close_view(viewID):
    client = get_client()
    return client.closeView(viewID)

#def set_view_index(viewID, datas):
#    '''
#    设置模型指标属性
#    index: { "output1": { "datatype": se::OutputDataType } }
#    '''
#    client = get_client()
#    return client.setViewIndex(viewID, datas)

def push_view_data(viewID, datas):
    '''
    推送模型结果数据
    datas: { "timetags: [t1, t2, ...], "outputs": { "output1": [value1, value2, ...], ... }, "overwrite": "full/increase" }
    '''
    client = get_client()
    bresult = client.pushViewData(viewID, 'index', bson.BSON.encode(datas))
    return bson.BSON.decode(bresult)
