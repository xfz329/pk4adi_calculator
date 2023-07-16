#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   data_toolbar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QFileDialog

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon, PrimaryPushButton, SplitPushButton, PillPushButton, InfoBar, InfoBarPosition,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel)

from .toolbar import ToolBar
from .separator_widget import SeparatorWidget
from ...globalvar.vars import set_value, get_value

import pandas as pd

class DataToolBar(ToolBar):
    """ Data Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(title = title, subtitle = subtitle, parent=parent)

        self.openDataButton = PrimaryPushButton("打开文件", self, FluentIcon.DOCUMENT)
        self.separator1 = SeparatorWidget(self)
        self.toFirstButton = PrimaryPushButton("第一页", self)
        self.toPreviousButton = PrimaryPushButton("前一页", self)
        self.toNextButton = PrimaryPushButton("后一页", self)
        self.separator2 = SeparatorWidget(self)
        self.textButton = PillPushButton("text", self, FluentIcon.TAG)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)

        self.__initButtonLayout()
        self.__setPrimaryPushButtonVisible()


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
        self.textButton.setChecked(False)

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
        f = QFileDialog.getOpenFileName(None, "打开", "D:\\UrgeData\\Desktop", "csv or xls files (*.csv *.xls *xlsx)")
        file = f[0]
        if file == "":
            # self.log.error("未选择任何需要打开的文件！")
            return None
        # self.log.info("当前选中的需要打开文件为 " + file)
        print("当前选中的需要打开文件为 " + file)
        self.open(file)

    def open(self,file):
        df = None
        if file is None:
            # self.log.error("打开文件名为空！")
            return None
        if file.endswith(".csv"):
            df = pd.read_csv(file)
            # self.log.info("csv文件读取完成 "+file)
        elif file.endswith(".xls") or file.endswith(".xlsx"):
            df = pd.read_excel(file, None)
            # self.log.info("xls/xlsx文件读取完成 "+file)
        else:
            # self.log.warning("该文件类型暂不支持 "+file)
            return None
        print("read ok")
        set_value("data", df)
        if isinstance(df, dict) :
            set_value("workbooks", list(df.keys()))
            set_value("current_workbook_num", 0)
            n = len(list(df.keys()))
            set_value("total_workbook_num", n)
            if  n > 1 :
                self.toX(0)
                self.__setPrimaryPushButtonVisible(True)
        self.newDataReadSig.emit()

    def toX(self, x):
        set_value("current_workbook_num", x)
        workbooks = get_value("workbooks")
        text = "当前打开的工作簿为 " + workbooks[x] + " ( " + str(x + 1) +" / " + str(get_value("total_workbook_num")) + " )"
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

    def createTopRightInfoBar(self):
        InfoBar.success(
            title=self.tr('Lesson 3'),
            content=self.tr("Believe in the spin, just keep believing!"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )






