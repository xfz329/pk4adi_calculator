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

from common.style_sheet import StyleSheet
from globalvar.vars import set_value, get_value
from view.widget.output_toolbar import OutputToolBar

class OutputInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("output_interface")
        self.widget = QWidget(self)
        self.gridLayout = QGridLayout(self)

        self.toolBar = OutputToolBar(self.tr("Output"), self.tr("Display the output of last analysis command."), self)
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
        if self.work_type == "pk":
            self.table.setItemDelegate(PKTableItemDelegate(self.table))
        self.updateDataFrame(df)
        self.work_dir = get_value("last_work_dir")

    def updateDataFrame(self, df):
        row_num, col_num = df.shape
        self.table.setRowCount(row_num)
        self.table.setColumnCount(col_num)
        self.table.setHorizontalHeaderLabels(df.columns)
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

class PKTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        # pk_columns = [self.tr("Independent variables"), self.tr("Test variables"), self.tr("Error Detail"),
        #               "PK", "SE0", "SE1", self.tr("Jackknife"), "PKj", "SEj"]
        super().initStyleOption(option, index)
        if not index.column() in [2]:
            return
        option.palette.setColor(QPalette.Text, Qt.red)
        option.palette.setColor(QPalette.HighlightedText, Qt.red)

class PKSTableItemDelegate(TableItemDelegate):
    """ Custom table item delegate """

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        # pks_columns = [self.tr("Independent variables"), self.tr("Test variables 1"), self.tr("Test variables 2"),
        #                self.tr("Error of PK1"), self.tr("Error of PK2"), self.tr("Error of comparision"),
        #                "PKD", "SED", "ZD", self.tr("P value of norm"), self.tr("Comment 1"),
        #                "PKDJ", "SEDJ", "DF", "TD", self.tr("P value of t"), self.tr("Comment 2")]
        super().initStyleOption(option, index)
        column = index.column()
        if not column in [3, 4, 5]:
            return
        option.palette.setColor(QPalette.Text, Qt.red)
        option.palette.setColor(QPalette.HighlightedText, Qt.red)


