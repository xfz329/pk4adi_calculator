#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   data_toolbar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
import pandas as pd

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QFileDialog

from qfluentwidgets import ToolButton, FluentIcon, PrimaryPushButton, PillPushButton, InfoBar, ToolTipFilter

from globalvar.vars import set_value, get_value
from threads.openthread import OpenThread
from utils.logger import Logger
from view.widget.separator_widget import SeparatorWidget
from view.widget.toolbar import ToolBar

class DataToolBar(ToolBar):
    """ Data Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(title = title, subtitle = subtitle, parent=parent)

        self.openDataButton = PrimaryPushButton(self.tr("Open file"), self, FluentIcon.DOCUMENT)
        self.separator1 = SeparatorWidget(self)
        self.toFirstButton = PrimaryPushButton(self.tr("To the first"), self)
        self.toPreviousButton = PrimaryPushButton(self.tr("To the previous"), self)
        self.toNextButton = PrimaryPushButton(self.tr("To the next"), self)
        self.separator2 = SeparatorWidget(self)
        self.textButton = PillPushButton(self.tr("text"), self, FluentIcon.TAG)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)

        self.__initButtonLayout()
        self.__setPrimaryPushButtonVisible()

        self.openThread = OpenThread()
        self.openThread.finished_signal.connect(self.loadData)

        self.logger = Logger().get_logger()

    def __initButtonLayout(self):
        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.openDataButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.separator1, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.toFirstButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.toPreviousButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.toNextButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.separator2, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.textButton,0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.themeButton.clicked.connect(self.toggleTheme)
        self.openDataButton.clicked.connect(self.openData)
        self.toFirstButton.clicked.connect(self.toFirst)
        self.toNextButton.clicked.connect(self.toNext)
        self.toPreviousButton.clicked.connect(self.toPrevious)
        self.textButton.setCheckable(False)

    def __setPrimaryPushButtonVisible(self, v = False):
        self.separator1.setVisible(v)
        self.toFirstButton.setVisible(v)
        self.toNextButton.setVisible(v)
        self.toPreviousButton.setVisible(v)
        self.separator2.setVisible(v)
        self.textButton.setVisible(v)

    def openData(self):
        # file = r"D:\UrgeData\Desktop\pk_test\12.xlsx"
        self.__setPrimaryPushButtonVisible()
        f = QFileDialog.getOpenFileName(None, self.tr("OPen"), ".", self.tr("csv or xls files (*.csv *.xls *xlsx)"))
        file = f[0]
        if file == "":
            self.logger.error(self.tr("Selected nothing to open"))
            return None
        self.logger.info(self.tr("The selected file to open is {0} , try opening it in a new thread.").format(file))
        self.openThread.set_file(file)
        self.openThread.start()

    def loadData(self):
        df = self.openThread.get_ans()
        self.logger.info(self.tr("Load data read from the thread"))
        self.logger.debug(df)
        if isinstance(df, dict) :
            n = len(list(df.keys()))
            set_value("workbooks", df)
            set_value("workbook_names", list(df.keys()))
            set_value("total_workbook_num", n)
            self.logger.info(self.tr("The data contains multi-workbooks, the names listed as the following:"))
            self.logger.info(list(df.keys()))
            self.logger.info(self.tr("Display the first workbook."))
            self.toX(0)
            if  n > 1 :
                self.__setPrimaryPushButtonVisible(True)
        elif isinstance(df, pd.DataFrame):
            set_value("current_workbook", df)
            self.logger.info(self.tr("The data with single workbook has been displayed."))
            self.createTopRightInfoBar(self.tr("Success"), self.tr("Display the data in the file."))
            self.checkDataFrame()
            self.newDataReadSig.emit()
        else:
            return

    def toX(self, x):
        workbooks = get_value("workbooks")
        workbook_names = get_value("workbook_names")
        name = workbook_names[x]
        set_value("current_workbook_num", x)
        set_value("current_workbook_name", name)
        set_value("current_workbook", workbooks.get(name))
        self.checkDataFrame()
        text = self.tr("Workbook {0} ( {1} / {2} )").format(name, str(x+1), str(get_value("total_workbook_num")) )
        self.logger.info(self.tr("The workbook named {0} has been displayed.").format(name))
        self.createTopRightInfoBar(self.tr("Success"), self.tr("Display the workbook {0} in the file.").format(name))
        self.textButton.setText(text)
        self.newDataReadSig.emit()

    def toFirst(self):
        self.toX(0)

    def toNext(self):
        total = get_value("total_workbook_num")
        current = get_value("current_workbook_num")
        current = (current + 1) % total
        self.toX(current)

    def toPrevious(self):
        total = get_value("total_workbook_num")
        current = get_value("current_workbook_num")
        current = (current + total - 1) % total
        self.toX(current)

    def checkDataFrame(self):
        df = get_value("current_workbook")
        df.rename(columns=self.my_converter, inplace=True)
        set_value("current_workbook", df)

    def my_converter(self, col):
        if isinstance(col, int) or isinstance(col, float):
            return str(col)
        return col
