#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   data_toolbar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QFileDialog

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon, PrimaryPushButton, SplitPushButton, PillPushButton, InfoBar,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel)

from .toolbar import ToolBar
from .separator_widget import SeparatorWidget
from ...globalvar.vars import set_value, get_value
from ...thread.openthread import OpenThread
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

        self.openThread = OpenThread()
        self.openThread.finished_signal.connect(self.loadData)

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
        f = QFileDialog.getOpenFileName(None, "打开", "D:\\UrgeData\\Desktop", "csv or xls files (*.csv *.xls *xlsx)")
        file = f[0]
        if file == "":
            # self.log.error("未选择任何需要打开的文件！")
            return None
        # self.log.info("当前选中的需要打开文件为 " + file)
        print("当前选中的需要打开文件为 " + file)
        self.openThread.set_file(file)
        self.openThread.start()

    def loadData(self):
        df = self.openThread.get_ans()
        if isinstance(df, dict) :
            n = len(list(df.keys()))
            set_value("workbooks", df)
            set_value("workbook_names", list(df.keys()))
            set_value("total_workbook_num", n)
            self.toX(0)
            if  n > 1 :
                self.__setPrimaryPushButtonVisible(True)
        elif isinstance(df, pd.DataFrame):
            set_value("current_workbook", df)
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
        text = "当前打开的工作簿为 " + name + " ( " + str(x + 1) +" / " + str(get_value("total_workbook_num")) + " )"
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
        self.createTopRightInfoBar("成功","就是简简单单的一次运行成功")

    def checkDataFrame(self):
        df = get_value("current_workbook")
        col = df.columns.tolist()
        if len(col) != len(set(col)):
            self.createTopRightInfoBar("警告","当前工作簿中列名存在同名！这可能引发后续计算错误或程序崩溃！", InfoBar.warning, 4000)
        not_str = False
        for c in df.columns:
            if not isinstance(c, str):
                not_str = True
        if not_str:
            self.createTopRightInfoBar("警告", "当前工作簿中列名存在纯数字！这可能引发后续计算错误或程序崩溃！", InfoBar.warning, 4000)

