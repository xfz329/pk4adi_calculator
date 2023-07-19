#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   output_interface.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import pandas as pd
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidgetItem, QSizePolicy, QStyleOptionViewItem
from qfluentwidgets import TableWidget, TableItemDelegate
from .widget.output_toolbar import OutputToolBar
from ..common.style_sheet import StyleSheet
from ..globalvar.vars import get_value

class OutputInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("output_interface")
        self.widget = QWidget(self)
        self.gridLayout = QGridLayout(self)

        self.toolBar = OutputToolBar("Output", "选择需要分析的数据", self)
        self.table = TableWidget(self)
        self.work_dir = None
        self.work_type = None

        self.__initWidget()
        self.initTable()

    def __initWidget(self):
        self.gridLayout.addWidget(self.toolBar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 1)
        StyleSheet.GALLERY_INTERFACE.apply(self)

    def initTable(self, str = None):
        self.table.verticalHeader().hide()
        cls = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
        df = pd.DataFrame(columns=cls, index=range(1, 4))
        df = df.fillna("")
        self.updateDataFrame(df)

    def updateData(self):
        self.work_type = get_value("last_work")
        df = get_value(self.work_type)
        if self.work_type == "pks":
            self.table.setItemDelegate(PKSTableItemDelegate(self.table))
        self.updateDataFrame(df)
        self.work_dir = get_value("last_work_dir")

    def updateDataFrame(self, df):
        row_num, col_num = df.shape
        self.table.setRowCount(row_num)
        self.table.setColumnCount(col_num)
        columns = []
        for c in df.columns:
            if not isinstance(c, str):
                columns.append(str(c))
            else:
                columns.append(c)
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for i in range(row_num):
            for j in range(col_num):
                item = df.iloc[i, j]
                if not isinstance(item, str):
                    item = str(item)
                self.table.setItem(i, j, QTableWidgetItem(item))
            self.table.setRowHeight(i, 30)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

# class PKTableItemDelegate(TableItemDelegate):
#     """ Custom table item delegate """
#
#     def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
#         # pk_columns = ["Independent variables", "Test variables", "PK", "SE0", "SE1", "Jackknife", "PKj", "SEj",
#         #               "Error Detail"]
#         super().initStyleOption(option, index)
#         if not index.column() in []:
#             return
#         option.palette.setColor(QPalette.Text, Qt.red)
#         option.palette.setColor(QPalette.HighlightedText, Qt.red)
#
class PKSTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        # pks_columns = ["Independent variables", "Test variables 1", "Test variables 2",
        #                "PKD", "SED", "ZD", "P value of norm", "Comment 1",
        #                "PKDJ", "SEDJ", "DF", "TD", "P value of t", "Comment 2", "Error 1", "Error 2"]
        super().initStyleOption(option, index)
        column = index.column()
        if not column in [14, 15]:
            return
        option.palette.setColor(QPalette.Text, Qt.red)
        option.palette.setColor(QPalette.HighlightedText, Qt.red)


