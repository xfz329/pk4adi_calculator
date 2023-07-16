# coding:utf-8

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from .frame.frame import Frame
from .frame.listframe import ListFrame
from .widget.operate_toolbar import OperateToolBar

import pandas as pd

from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from .widget.data_toolbar import DataToolBar
from ..common.style_sheet import StyleSheet
from PyQt5.QtWidgets import QTableWidgetItem, QSizePolicy, QListWidgetItem
from qfluentwidgets import TableWidget, ListWidget, PrimaryPushButton

from ..globalvar.vars import get_value

class OperateInterface(QWidget):
    """ View interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("operate_interface")
        self.widget = QWidget(self)
        self.gridLayout = QGridLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.toolBar = OperateToolBar("Analysis", "对已选数据进行分析", self)
        self.listWidget_all = ListWidget(self)
        self.listWidget_y = ListWidget(self)
        self.listWidget_x = ListWidget(self)

        self.frame_all = Frame(self)
        self.frame_x = Frame(self)
        self.frame_y = Frame(self)

        self.pushButton_y = PrimaryPushButton("添加", self)
        self.pushButton_all = PrimaryPushButton("添加全部", self)
        self.pushButton_x = PrimaryPushButton("添加", self)

        self.list_all = []
        self.list_x = []
        self.list_y = []
        self.list_empty = []

        self.__initWidget()
        self.__initListWidgets()

    def __initWidget(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_y.sizePolicy().hasHeightForWidth())
        self.listWidget_y.setSizePolicy(sizePolicy)

        self.frame_all.addWidget(self.listWidget_all)
        self.frame_x.addWidget(self.listWidget_x)
        self.frame_y.addWidget(self.listWidget_y)

        self.gridLayout.addWidget(self.toolBar, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.frame_all, 1, 0, 2, 1)
        self.gridLayout.addWidget(self.pushButton_y, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_y, 1, 2, 1, 1)

        self.verticalLayout.addWidget(self.pushButton_all)
        self.verticalLayout.addWidget(self.pushButton_x)
        self.gridLayout.addLayout(self.verticalLayout, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_x, 2, 2, 1, 1)

    def __initListWidgets(self):
        self.setList(self.listWidget_x, self.list_empty)
        self.setList(self.listWidget_y, self.list_empty)

        pass

    def setList(self, list_widget, list_content):
        for content in list_content:
            list_widget.addItem(QListWidgetItem(content))
        print(list_widget.height())
        print(list_widget.width())












