#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   operate_toolbar.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from PyQt5.QtCore import Qt

from qfluentwidgets import ToolButton, FluentIcon, PrimaryPushButton, PillPushButton, ToolTipFilter, IndeterminateProgressBar

from view.widget.toolbar import ToolBar
from view.widget.separator_widget import SeparatorWidget

class OperateToolBar(ToolBar):
    """ Operate Tool bar """

    def __init__(self, title, subtitle, parent=None):
        super().__init__(title = title, subtitle = subtitle, parent=parent)

        self.calcaulateButton = PrimaryPushButton(self.tr("Calculate PKs"), self)
        self.compareButton = PrimaryPushButton(self.tr("Compare PKs"), self)
        self.separator1 = SeparatorWidget(self)
        self.resetButton = PrimaryPushButton(self.tr("Reset variables"), self)
        self.separator2 = SeparatorWidget(self)
        self.textButton = PillPushButton(self.tr("Calculating"), self, FluentIcon.TAG)
        self.progressbar = IndeterminateProgressBar(self)
        self.themeButton = ToolButton(FluentIcon.CONSTRACT, self)

        self.__initButtonLayout()

    def __initButtonLayout(self):
        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.calcaulateButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.compareButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.separator1, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.resetButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.separator2, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.textButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.progressbar, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.themeButton, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.themeButton.installEventFilter(ToolTipFilter(self.themeButton))
        self.themeButton.clicked.connect(self.toggleTheme)
        self.textButton.setCheckable(False)
        self.showProgressBar(False)

    def showProgressBar(self, visiable):
        self.separator2.setVisible(visiable)
        self.progressbar.setVisible(visiable)
        self.textButton.setVisible(visiable)
        if visiable:
            self.progressbar.resume()
        else:
            self.progressbar.pause()
