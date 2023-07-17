#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pkthread.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from ..globalvar.vars import set_value, get_value
from .basicthread import BasicThread
from PyQt5.QtCore import pyqtSignal
class PKThread(BasicThread):
    warn_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, name = "pk"):
        super().__init__(name)

    def run(self):
        import time
        time.sleep(10)
        self.finished_signal.emit()
