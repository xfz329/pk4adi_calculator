#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from qtpandas.models.DataFrameModel import DataFrameModel
from qtpandas.views.DataTableView import DataTableWidget

from mythread.task_open import TaskOpen
from myui.analysis import Ui_MainWindow as aum
from myui.main_basic import Ui_MainWindow
from myui.about import Ui_MainWindow as abum
from utils.logger import Logger


class Ui_My_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.current_file = None
        self.log = Logger().get_logger()
        self.taskOpen = TaskOpen(self.get_data, "open")
        self.AnalysisWindow = None
        self.AboutWindow = None
        self.qtpandas_widget = None
        self.data = None
        self.data_dict = None
        self.sheet_name = None
        self.sheet_num = 0

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./figures/pk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.init_ptpandas_widget(MainWindow)

        self.action_open.triggered.connect(self.open)
        self.action_new_win_analysis.triggered.connect(self.show_analysis)
        self.action_about.triggered.connect(self.show_about)
        self.action_logs.triggered.connect(self.show_logs)
        self.action_previous_sheeet.triggered.connect(self.to_previous_sheet)
        self.action_next_sheet.triggered.connect(self.to_next_sheet)
        self.action_first_sheet.triggered.connect(self.to_first_sheet)
        self.action_previous_sheeet.setEnabled(False)
        self.action_next_sheet.setEnabled(False)
        self.action_first_sheet.setEnabled(False)

        self.update_statusbar("系统初始化完毕")

    def init_ptpandas_widget(self, MainWindow):
        widget = DataTableWidget()
        widget.setButtonsVisible(False)
        widget.tableView.setSortingEnabled(False)
        model = DataFrameModel()
        widget.setViewModel(model)
        df = pd.DataFrame(columns=['A', 'B', 'C', 'D'], index=range(1, 4))
        model.setDataFrame(df)
        MainWindow.setCentralWidget(widget)
        self.qtpandas_widget = widget

    def open(self):
        self.action_previous_sheeet.setEnabled(False)
        self.action_next_sheet.setEnabled(False)
        self.action_first_sheet.setEnabled(False)
        self.taskOpen.set_worker()
        self.log.debug("开启新线程读取文件")

    def show_analysis(self):
        self.AnalysisWindow = aum(self.data)
        self.AnalysisWindow.show()
        self.log.info("打开数据分析窗口")

    def show_about(self):
        self.AboutWindow = abum("about")
        self.AboutWindow.show()

    def show_logs(self):
        self.AboutWindow = abum("logs")
        self.AboutWindow.show()

    def get_data(self):
        data = self.taskOpen.get_ans()
        self.log.info(data)
        if isinstance(data, dict):
            QMessageBox.information(None, "打开文件成功", "已打开包含多个sheet的xls/xlsx文件。当前显示该文件的第一个sheet。", QMessageBox.Ok)
            self.action_previous_sheeet.setEnabled(True)
            self.action_next_sheet.setEnabled(True)
            self.action_first_sheet.setEnabled(True)

            self.data_dict = data
            self.sheet_name = list(data.keys())
            self.to_sheet_n(0)
        else:
            self.update_data(data)
            QMessageBox.information(None, "打开文件成功", "打开文件成功，其数据已显示。", QMessageBox.Ok)

    def update_data(self, data):
        if isinstance(data,pd.DataFrame):
            self.qtpandas_widget.model().setDataFrame(data)
            self.data = data

    def to_first_sheet(self):
        self.sheet_num = 0
        self.to_sheet_n(self.sheet_num)

    def to_previous_sheet(self):
        n = len(self.sheet_name)
        self.sheet_num = (self.sheet_num + n - 1) % n
        self.to_sheet_n(self.sheet_num)

    def to_next_sheet(self):
        n = len(self.sheet_name)
        self.sheet_num = (self.sheet_num + 1) % n
        self.to_sheet_n(self.sheet_num)

    def to_sheet_n(self, n):
        sheet = self.sheet_name[n]
        df = self.data_dict.get(sheet, None)
        self.update_data(df)
        self.update_statusbar("当前显示已打开文件的sheet为"+sheet)

    def update_statusbar(self,msg):
        self.statusbar.clearMessage()
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString("HH:mm:ss")
        self.statusbar.showMessage(text+"  "+msg, 5000)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_My_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
    MainWindow.show()
    sys.exit(app.exec_())
