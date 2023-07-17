# coding:utf-8

from .frame.frame import Frame
from .widget.operate_toolbar import OperateToolBar

import pandas as pd

from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from .widget.data_toolbar import DataToolBar
from ..common.style_sheet import StyleSheet
from PyQt5.QtWidgets import QTableWidgetItem, QSizePolicy, QListWidgetItem, QAbstractItemView
from qfluentwidgets import TableWidget, ListWidget, PrimaryPushButton, PillPushButton, FluentIcon

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

        self.variables_all = PillPushButton("所有变量", self, FluentIcon.TAG)
        self.variables_x = PillPushButton("检验变量", self, FluentIcon.TAG)
        self.variables_y = PillPushButton("独立变量", self, FluentIcon.TAG)

        self.list_all = []
        self.list_x = []
        self.list_y = []
        self.list_empty = []

        self.add_to_x = True
        self.add_to_y = True

        self.__initWidget()
        self.__initListWidgets()
        self.__initConnects()

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
        self.gridLayout.addWidget(self.frame_all, 2, 0, 4, 1)
        self.gridLayout.addWidget(self.pushButton_y, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_y, 3, 2, 1, 1)

        self.gridLayout.addWidget(self.variables_all, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.variables_y, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.variables_x, 4, 2, 1, 1)

        self.verticalLayout.addWidget(self.pushButton_all)
        self.verticalLayout.addWidget(self.pushButton_x)
        self.gridLayout.addLayout(self.verticalLayout, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_x, 5, 2, 1, 1)

        self.variables_all.setCheckable(False)
        self.variables_y.setCheckable(False)
        self.variables_x.setCheckable(False)

        self.listWidget_all.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_x.setSelectionMode(QAbstractItemView.ExtendedSelection)

        StyleSheet.GALLERY_INTERFACE.apply(self)

    def __initListWidgets(self):
        self.pushButton_x.setEnabled(False)
        self.pushButton_y.setEnabled(False)
        self.pushButton_all.setEnabled(False)

        self.resetLists()

    def __initButtons(self):
        self.pushButton_x.setEnabled(True)
        self.pushButton_y.setEnabled(True)
        self.pushButton_all.setEnabled(True)

        self.pushButton_x.setText("添加")
        self.pushButton_y.setText("添加")
        self.pushButton_all.setText("添加全部")

        self.add_to_x = True
        self.add_to_y = True

    def __initConnects(self):
        self.toolBar.openDirButton.clicked.connect(self.openOutputDir)
        self.toolBar.resetButton.clicked.connect(self.resetLists)
        self.listWidget_all.clicked.connect(self.__initButtons)
        self.listWidget_x.clicked.connect(self.remove_from_x)
        self.listWidget_y.clicked.connect(self.remove_from_y)
        self.pushButton_x.clicked.connect(self.clicked_button_x)
        self.pushButton_y.clicked.connect(self.clicked_button_y)
        self.pushButton_all.clicked.connect(self.clicked_button_all)

    def resetLists(self):
        self.setList(self.listWidget_x, self.list_x)
        self.setList(self.listWidget_y, self.list_y)
        self.setList(self.listWidget_all, self.list_all)

    def setList(self, list_widget, list_content):
        while list_widget.count() > 0:
            list_widget.takeItem(0)
        for content in list_content:
            list_widget.addItem(QListWidgetItem(content))
        list_widget.clearSelection()

    def updateList(self):
        df = get_value("current_workbook")
        self.list_all = df.columns
        self.resetLists()
        self.__initButtons()

    def openOutputDir(self):
        # os.startfile(self.out_dir)
        print("open")
        pass

    def remove_from_x(self):
        self.pushButton_x.setText("移除")
        self.pushButton_all.setText("移除全部")
        self.add_to_x = False

    def remove_from_y(self):
        self.pushButton_y.setText("移除")
        self.add_to_y = False

    def exchange_selected(self, source, destination):
        selected = source.selectedIndexes()
        idx = [x.row() for x in selected]
        idx.sort(reverse=True)
        for num in idx:
            it = source.takeItem(num)
            destination.addItem(it)
        source.clearSelection()
        destination.clearSelection()

    def remove_all(self, source, destination):
        while source.count() > 0 :
            it = source.takeItem(0)
            destination.addItem(it)

    def clicked_button_x(self):
        if self.add_to_x:
            self.exchange_selected(self.listWidget_all, self.listWidget_x)
        else:
            self.exchange_selected(self.listWidget_x, self.listWidget_all)

    def clicked_button_y(self):
        if self.add_to_y:
            if self.listWidget_y.count() == 0 and len(self.listWidget_all.selectedItems()) == 1:
                self.exchange_selected(self.listWidget_all, self.listWidget_y)
            else:
                pass
        else:
            self.exchange_selected(self.listWidget_y, self.listWidget_all)

    def clicked_button_all(self):
        if self.add_to_x:
            self.remove_all(self.listWidget_all, self.listWidget_x)
        else:
            self.remove_all(self.listWidget_x, self.listWidget_all)













