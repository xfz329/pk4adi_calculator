#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   output_toolbar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
import os

from PyQt5.QtCore import Qt

from qfluentwidgets import ToolButton, FluentIcon, PrimaryPushButton, PillPushButton, InfoBar, ToolTipFilter

from globalvar.vars import set_value, get_value
from common.config import cfg
from utils.logger import Logger
from view.widget.toolbar import ToolBar
from view.widget.separator_widget import SeparatorWidget
from view.window.demo_window import Demo_Window

class OutputToolBar(ToolBar):
    """ Output Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(title = title, subtitle = subtitle, parent=parent)

        self.openRootDirButton = PrimaryPushButton("Open the root dir", self, FluentIcon.BOOK_SHELF)
        self.openDirButton = PrimaryPushButton("Open the subdir", self, FluentIcon.FOLDER)
        self.editButton = PrimaryPushButton("Take notes", self, FluentIcon.EDIT)
        self.separator = SeparatorWidget(self)
        self.textButton = PillPushButton("Opened nothing", self, FluentIcon.TAG)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)

        self.logger = Logger().get_logger()

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
        self.logger.info("Open the sub folder of the output.")

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
        self.logger.info("Open the root folder of the output.")