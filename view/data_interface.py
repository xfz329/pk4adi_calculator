# coding:utf-8

import pandas as pd

from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidgetItem, QSizePolicy

from qfluentwidgets import TableWidget

from common.style_sheet import StyleSheet
from globalvar.vars import get_value
from view.widget.data_toolbar import DataToolBar

class DataInterface(QWidget):
    """ Data interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("data_interface")
        self.widget = QWidget(self)
        self.gridLayout = QGridLayout(self)

        self.toolBar = DataToolBar("Data", "Select file to conduct analysis.", self)
        self.table = TableWidget(self)

        self.__initWidget()
        self.__initTable()

    def __initWidget(self):
        self.gridLayout.addWidget(self.toolBar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 1)
        StyleSheet.GALLERY_INTERFACE.apply(self)
        self.toolBar.newDataReadSig.connect(self.updateData)

    def __initTable(self):
        self.table.verticalHeader().hide()
        cls = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
        df = pd.DataFrame(columns=cls, index=range(1, 4))
        df = df.fillna("")
        self.updateDataFrame(df)


    def updateData(self):
        df = get_value("current_workbook")
        self.updateDataFrame(df)

    def updateDataFrame(self, df):
        row_num, col_num = df.shape
        self.table.setRowCount(row_num)
        self.table.setColumnCount(col_num)
        columns =[]
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









