#   -*- coding:utf-8 -*-
#   The changelogs.py in FeatureAnalyzer
#   created by Jiang Feng(silencejiang@zju.edu.cn)
#   created at 13:41 on 2022/3/27

from PyQt5 import QtCore

from help.changelogs.changelogs_basic import Ui_MainWindow
from template.changelogs_template import Template


class Ui_Changelogs_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_Changelogs_MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.label.setText(self.getlogs())
        self.label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

    def getlogs(self):
        t = Template()
        return t.get()