#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   openthread.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
import pandas as pd
from .basicthread import BasicThread

class OpenThread(BasicThread):

    def __init__(self, file = None, name = "open_thread"):
        super().__init__(name)
        self.file = file

    def set_file(self, file):
        self.file = file

    def run(self):
        file = self.file
        print(file)
        if file is None:
            # self.log.error("打开文件名为空！")
            ans = None
        if file.endswith(".csv"):
            ans = pd.read_csv(file)
            # self.log.info("csv文件读取完成 "+file)
        elif file.endswith(".xls") or file.endswith(".xlsx"):
            ans = pd.read_excel(file, None)
            # self.log.info("xls/xlsx文件读取完成 "+file)
        else:
            # self.log.warning("该文件类型暂不支持 "+file)
            ans= None
        self.ans = ans
        self.finished_signal.emit()