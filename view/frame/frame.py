#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   frame.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

from PyQt5.QtWidgets import QFrame, QHBoxLayout

from common.style_sheet import StyleSheet

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)