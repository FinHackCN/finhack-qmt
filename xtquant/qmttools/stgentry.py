#coding:utf-8

import os, sys
import types

from .functions import *
from .contextinfo import ContextInfo
from .stgframe import StrategyLoader


def run_file(user_script, param = {}):
    pypath = param.get('pythonpath')
    if pypath:
        lib_search = [os.path.abspath(p) for p in pypath.split(';')]
        sys.path = lib_search + [p for p in sys.path if p not in lib_search]

    user_module = compile(open(user_script, 'rb').read(), user_script, 'exec', optimize = 2)
    #print({'user_module': user_module})

    user_locals = {}

    try:
        pywentrance = param.get('pywentrance', '')
        user_variable = compile(open(os.path.join(pywentrance, "..", "user_config.py"), "rb").read(),
                                "user_config.py", 'exec', optimize=2)
        exec(user_variable, globals(), user_locals)
    except Exception as e:
        pass

    exec(user_module, globals(), user_locals)
    #print('user_locals', user_locals)

    globals().update(user_locals)

    _C = ContextInfo()
    _C._param = param
    _C.user_script = user_script

    def try_set_func(C, func_name):
        func = user_locals.get(func_name)
        if func:
            C.__setattr__(func_name, types.MethodType(func, C))
        return

    try_set_func(_C, 'init')
    try_set_func(_C, 'after_init')
    try_set_func(_C, 'handlebar')
    try_set_func(_C, 'stop')

    try_set_func(_C, 'account_callback')
    try_set_func(_C, 'order_callback')
    try_set_func(_C, 'deal_callback')
    try_set_func(_C, 'position_callback')
    try_set_func(_C, 'orderError_callback')

    loader = StrategyLoader()

    loader.C = _C

    loader.init()
    loader.start()
    loader.run()
    loader.stop()
    loader.shutdown()

    return
