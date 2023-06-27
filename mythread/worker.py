#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   worker.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
import traceback
from qtpandas.models.ProgressThread import ProgressWorker
import time
from utils.logger import Logger

class Worker(ProgressWorker):
    def __init__(self, name):
        super(Worker, self).__init__(name)
        self.log = Logger().get_logger()
        self.ans = None
        self.kwargs = []
        self.pwargs = ()

    def get_ans(self):
        return self.ans

    def set_parameters(self, * pwargs, ** kwargs):
        self.pwargs = pwargs
        self.kwargs = kwargs

    def run(self):
        self.log.debug("开始处理任务函数 "+time.strftime("%H:%M:%S",time.localtime()))
        try:
            self.ans = self.handle_job(* self.pwargs, ** self.kwargs)
        except Exception as e:
            self.log.error(e)
            info = traceback.format_exc()
            self.log.error("任务函数处理出现错误！以下为详细信息")
            self.log.error(info)
            self.ans = {"error":e,"info":info}
        self.log.debug("任务函数处理完毕 " + time.strftime("%H:%M:%S", time.localtime()))

    def handle_job(self, * pwargs, ** kwargs):
        pass

    def set_job(self, func):
        self.handle_job = func