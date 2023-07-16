# coding:utf-8

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QToolButton, QPushButton, QTableView
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from .frame.tableframe import TableFrame
from .widget.data_toolbar import DataToolBar
from .widget.example_card import ExampleCard
from .widget.toolbar import ToolBar
from ..common.style_sheet import StyleSheet
from qfluentwidgets import TableWidget
from PyQt5.QtWidgets import QTableWidgetItem, QSizePolicy
from qfluentwidgets import TableWidget

from ..globalvar.vars import get_value

import pandas as pd

class DataInterface(QWidget):
    """ Data interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.widget = QWidget(self)
        self.gridLayout = QGridLayout(self)
        self.setObjectName("datainterface")

        self.table = TableWidget(self)

        self.gridLayout.setObjectName("gridLayout")
        self.toolBar = DataToolBar("Data", "选择需要分析的数据", self)
        self.gridLayout.addWidget(self.toolBar, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 1)



        self.table.verticalHeader().hide()
        cls = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
        df = pd.DataFrame(columns=cls, index=range(1, 4))
        df = df.fillna("")
        self.updateDataFrame(df)

        StyleSheet.GALLERY_INTERFACE.apply(self)
        self.toolBar.newDataReadSig.connect(self.updateData)

    def updateData(self):
        data = get_value("data")
        print(type(data))
        if isinstance(data, dict):
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
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
            self.table.setRowHeight(i, 30)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        # self.table.setFixedHeight(30 * (row_num + 3))








