#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   demo_dialog.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
import time
from os.path import join
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QTextBlockFormat
from qfluentwidgets import PrimaryPushButton
from qframelesswindow import FramelessWindow
from ...globalvar.vars import get_value


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(-1, 32, -1, -1)
        # self.plainTextEdit = PlainTextEdit(Form)
        self.edit = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit.sizePolicy().hasHeightForWidth())
        self.edit.setSizePolicy(sizePolicy)
        self.edit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.edit.setFocus()
        self.gridLayout.addWidget(self.edit, 0, 0, 1, 2)
        self.okButton = PrimaryPushButton("OK", Form)
        self.gridLayout.addWidget(self.okButton, 1, 0, 1, 1)
        self.cancelButton = PrimaryPushButton("Cancel", Form)
        self.gridLayout.addWidget(self.cancelButton, 1, 1, 1, 1)
        self.edit.setPlaceholderText("Just write some demo here.")


class Demo_Window(FramelessWindow, Ui_Form):
    text_signal = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.clickedOK)

    def clickedOK(self):
        dir = get_value("last_work_dir")
        name = time.strftime("%H-%M-%S", time.localtime()) + "_Demo.txt"
        full_name = join(dir, name)
        # text = self.plainTextEdit.toPlainText()
        text = self.edit.toPlainText()
        with open(full_name, 'a+', encoding='utf-8') as fp:
            fp.write(text)
            fp.close()
        self.text_signal.emit("The demo have been saved as "+full_name)
        self.close()

