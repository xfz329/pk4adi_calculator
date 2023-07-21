#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   globalvar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

def init_():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value
    # log.debug("set value "+ name + " to value " +str(value))
    # log.debug(_global_dict)
    # print(("set value "+ name + " to value " +str(value)))


def get_value(name, defValue = None):
    # log.debug("get value "+ name )
    # log.debug(_global_dict)
    try:
        return _global_dict[name]
    except KeyError:
        # log.error("no values matched key " + name )
        return defValue

def delete_value(name):
    # log.debug("delete value " + name)
    try:
        del _global_dict[name]
        # log.debug(_global_dict)
    except KeyError:
        # log.error("no values matched key " + name)
        return

def get_dict():
    return _global_dict