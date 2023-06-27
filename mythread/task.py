#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   task.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from qtpandas.models.ProgressThread import createThread
from mythread.worker import Worker
from utils.logger import Logger


class Task:

    def __init__(self,func,worker_name):
        self.worker = Worker(worker_name)
        self.thread = createThread(None, self.worker)
        self.worker.finished.connect(func)
        self.log = Logger().get_logger()

    def get_ans(self):
        return self.worker.get_ans()

    def set_worker(self,func,* pwargs, ** kwargs):
        self.worker.set_job(func)
        self.worker.set_parameters(* pwargs,**kwargs)
        self.log.info("The work job has been bounded to " + str(self.worker.handle_job))
        self.log.info("show pwargs")
        for l in pwargs:
            self.log.info(type(l))
            self.log.info(l)
            # if tp is not pd.core.frame.DataFrame:
            #     self.log.info("value is " + str(l)+" , type is "+str(tp))
            # else:
            #     self.log.info(" is a DataFrame")
        self.log.info("show kwargs")
        for key in kwargs.keys():
            self.log.info(type(key))
            if key != "data":
                self.log.info("key is "+key+" , value is "+str(kwargs[key]))
        self.thread.start()