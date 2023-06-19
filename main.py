#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from qtpandas.models.DataFrameModel import DataFrameModel
from qtpandas.views.DataTableView import DataTableWidget

from mythread.task_open import TaskOpen
from myui.analysis import Ui_MainWindow as aum
from myui.main_basic import Ui_MainWindow
from utils.logger import Logger


class Ui_My_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.current_file = None
        self.log = Logger().get_logger()
        self.taskOpen = TaskOpen(self.update_data, "open")
        self.AnalysisWindow = None
        self.qtpandas_widget = None
        self.data = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.init_ptpandas_widget(MainWindow)
        self.action_open.triggered.connect(self.open)
        self.action_new_win_analysis.triggered.connect(self.show_analysis)

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
        self.taskOpen.set_worker()

    def show_analysis(self):
        self.AnalysisWindow = aum(self.data)
        self.AnalysisWindow.show()

    def update_data(self):
        df = self.taskOpen.get_ans()
        if df is not None:
            self.qtpandas_widget.model().setDataFrame(df)
            self.data = df

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_My_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
    MainWindow.show()
    sys.exit(app.exec_())
