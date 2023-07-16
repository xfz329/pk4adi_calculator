#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   tableframe.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

from PyQt5.QtWidgets import QTableWidgetItem, QSizePolicy
from qfluentwidgets import TableWidget

from .frame import Frame
from ...globalvar.vars import get_value

import pandas as pd

class TableFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = TableWidget(self)
        self.addWidget(self.table)
        self.table.verticalHeader().hide()
        cls = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
        df = pd.DataFrame(columns=cls, index=range(1, 4))
        df = df.fillna("")
        self.updateDataFrame(df)

    def updateData(self):
        data = get_value("data")
        print(type(data))
        if isinstance(data,dict):
            current = get_value("current_workbook_num")
            workbooks = get_value("workbooks")
            sheet = workbooks[current]
            self.updateDataFrame(data.get(sheet))
        if isinstance(data, pd.DataFrame):
            self.updateDataFrame(data)

    def updateDataFrame(self, df):
        row_num, col_num = df.shape
        self.table.setRowCount(row_num)
        self.table.setColumnCount(col_num)
        print(df.columns)
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for i in range(row_num):
            for j in range(col_num):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i,j])))
            self.table.setRowHeight(i, 30)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setFixedHeight(30 * (row_num + 3))




