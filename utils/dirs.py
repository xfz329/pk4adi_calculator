#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   dirs.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

from pathlib import Path
import os, sys

BASE_DIR = Path(__file__).resolve().parent.parent

def get_out_dir():
    print(BASE_DIR)
    OUT_PATH = os.path.join(BASE_DIR, 'out')
    print(OUT_PATH)
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)
    return OUT_PATH

def init_log_files():
    LOG_PATH = os.path.join(BASE_DIR,'log')
    print(LOG_PATH)
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    DEBUG_FILE = os.path.join(LOG_PATH,'debug.log')
    WARN_FILE = os.path.join(LOG_PATH,'warn.log')
    INFO_FILE = os.path.join(LOG_PATH,'info.log')
    ERROR_FILE = os.path.join(LOG_PATH,'error.log')
    FILES = [DEBUG_FILE, WARN_FILE, INFO_FILE, ERROR_FILE]
    KEYS = ['debug', 'warn', 'info', 'error']
    DICT = { KEYS[i] : FILES[i] for i in range(len(KEYS))}

    for f in FILES:
        if not os.path.exists(f):
            if str(sys.platform).startswith('win'):
                with open(f, 'a+') as fp:
                    fp.close()
            else:
                os.mknod(f)
    return DICT

if __name__ == "__main__":
    print(init_log_files())

