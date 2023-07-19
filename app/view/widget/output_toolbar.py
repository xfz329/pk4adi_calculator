#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   output_toolbar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QFileDialog

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon, PrimaryPushButton, SplitPushButton, PillPushButton, IndeterminateProgressBar,InfoBar,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel)

from .toolbar import ToolBar
from .separator_widget import SeparatorWidget
from ...globalvar.vars import set_value, get_value
from ...common.config import cfg
from ...thread.openthread import OpenThread
from ..window.demo_window import Demo_Window
import pandas as pd
import os

class OutputToolBar(ToolBar):
    """ Output Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(title = title, subtitle = subtitle, parent=parent)

        self.openRootDirButton = PrimaryPushButton("打开输出根文件夹", self, FluentIcon.BOOK_SHELF)
        self.openDirButton = PrimaryPushButton("打开输出文件夹", self, FluentIcon.DOCUMENT)
        self.editButton = PrimaryPushButton("我想备注", self, FluentIcon.EDIT)
        self.separator = SeparatorWidget(self)
        self.textButton = PillPushButton("未打开任何文件", self, FluentIcon.TAG)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)

        self.__initButtonLayout()

    def __initButtonLayout(self):
        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.openRootDirButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.openDirButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.editButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.separator, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.textButton,0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.themeButton.clicked.connect(self.toggleTheme)
        self.openRootDirButton.clicked.connect(self.openRootDir)
        self.openDirButton.clicked.connect(self.openDir)
        self.editButton.clicked.connect(self.edit)
        self.openDirButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.textButton.setCheckable(False)

    def enable_buttons(self):
        self.openDirButton.setEnabled(True)
        self.editButton.setEnabled(True)

    def openDir(self):
        os.startfile(get_value("last_work_dir"))

    def edit(self):
        d = Demo_Window()
        d.text_signal.connect(self.showInfoBar)
        d.show()

    def changeText(self, str):
        self.textButton.setText(str)

    def showInfoBar(self, str):
        self.createTopRightInfoBar("Success",str, InfoBar.success)

    def openRootDir(self):
        os.startfile(cfg.get(cfg.outputFolder))