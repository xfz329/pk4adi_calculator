#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   openthread.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
import pandas as pd

from thread.basicthread import BasicThread
from utils.logger import Logger

class OpenThread(BasicThread):

    def __init__(self, file = None, name = "open_thread"):
        super().__init__(name)
        self.file = file
        self.logger = Logger().get_logger()

    def set_file(self, file):
        self.file = file

    def run(self):
        file = self.file
        if file is None:
            self.logger.error(self.tr("The file name is empty!"))
            ans = None
        if file.endswith(".csv"):
            ans = pd.read_csv(file)
            self.logger.info(self.tr("The csv file {0} read finished.").format(file))
        elif file.endswith(".xls") or file.endswith(".xlsx"):
            ans = pd.read_excel(file, None)
            self.logger.info(self.tr("The xls/xlsx file {0} read finished.").format(file))
        else:
            self.logger.error(self.tr("The file {0} is not supported yet.").format(file))
            ans= None
        self.ans = ans
        self.finished_signal.emit()