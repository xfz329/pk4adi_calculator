#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   basicthread.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

from PyQt5.QtCore import QThread, pyqtSignal

class BasicThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.ans = None

    def do_work(self):
        self.start()
        self.finished_signal.emit()

    def run(self):
        pass

    def get_ans(self):
        return self.ans