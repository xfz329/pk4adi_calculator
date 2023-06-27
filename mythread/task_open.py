#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   task_open.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from mythread.task import Task


class TaskOpen(Task):

    def __init__(self,func,work_name):
        Task.__init__(self,func,work_name)

    def set_worker(self):
        self.worker.set_job(self.open)
        file = self.get_file_to_open()
        self.worker.set_parameters(file = file)
        self.log.debug("当前线程绑定的任务函数为" + str(self.worker.handle_job))
        self.thread.start()

    def get_file_to_open(self):
        # file = r"D:\UrgeData\Desktop\pk_test\12.xlsx"
        f = QFileDialog.getOpenFileName(None, "打开", "D:\\UrgeData\\Desktop", "csv or xls files (*.csv *.xls *xlsx)")
        file = f[0]
        if file == "":
            self.log.error("未选择任何需要打开的文件！")
            return None
        self.log.info("当前选中的需要打开文件为 " + file)
        return file

    def open(self,file):
        df = None
        if file is None:
            self.log.error("打开文件名为空！")
            return None
        if file.endswith(".csv"):
            df = pd.read_csv(file)
            self.log.info("csv文件读取完成 "+file)
        elif file.endswith(".xls") or file.endswith(".xlsx"):
            df = pd.read_excel(file, None)
            self.log.info("xls/xlsx文件读取完成 "+file)
        else:
            self.log.warning("该文件类型暂不支持 "+file)
        return df