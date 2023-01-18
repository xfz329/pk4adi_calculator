#   -*- coding:utf-8 -*-
#   The author.py in FeatureAnalyzer
#   created by Jiang Feng(silencejiang@zju.edu.cn)
#   created at 19:44 on 2022/3/26


from PyQt5 import QtCore, QtWidgets

from help.author.author_basic import Ui_MainWindow
from template.author_template import Template


class Ui_Author_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(Ui_Author_MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self,MainWindow):
        super().setupUi(MainWindow)
        self.label.setText(self.getAuthor())
        self.label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

    def getAuthor(self):
        t = Template()
        return t.get()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Author_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())