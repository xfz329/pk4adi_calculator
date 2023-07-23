# coding:utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSizePolicy, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import pyqtSignal

from qfluentwidgets import ListWidget, PrimaryPushButton, PillPushButton, FluentIcon, InfoBar

from common.style_sheet import StyleSheet
from common.config import cfg
from globalvar.vars import set_value, get_value
from thread.pkthread import PKThread
from utils.logger import Logger
from view.frame import Frame
from view.widget.operate_toolbar import OperateToolBar

class OperateInterface(QWidget):
    """ View interface """
    calculate_started_signal = pyqtSignal(str)
    calculate_finished_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("operate_interface")
        self.widget = QWidget(self)
        self.gridLayout = QGridLayout(self)
        self.verticalLayout = QVBoxLayout()

        self.toolBar = OperateToolBar(self.tr("Variables"), self.tr("Calculate and compare the PK values of the variables."), self)
        self.listWidget_all = ListWidget(self)
        self.listWidget_y = ListWidget(self)
        self.listWidget_x = ListWidget(self)

        self.frame_all = Frame(self)
        self.frame_x = Frame(self)
        self.frame_y = Frame(self)

        self.pushButton_y = PrimaryPushButton(self.tr("Add"), self)
        self.pushButton_all = PrimaryPushButton(self.tr("Add all"), self)
        self.pushButton_x = PrimaryPushButton(self.tr("Add"), self)

        self.variables_all = PillPushButton(self.tr("Available variables"), self, FluentIcon.TAG)
        self.variables_x = PillPushButton(self.tr("Test variables"), self, FluentIcon.TAG)
        self.variables_y = PillPushButton(self.tr("Independent variables"), self, FluentIcon.TAG)

        self.list_all = []

        self.add_to_x = True
        self.add_to_y = True

        self.pkThread = PKThread()

        self.logger = Logger().get_logger()

        self.__initWidget()
        self.__initListWidgets()
        self.__initConnects()

    def __initWidget(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_y.sizePolicy().hasHeightForWidth())
        self.listWidget_y.setSizePolicy(sizePolicy)

        self.frame_all.addWidget(self.listWidget_all)
        self.frame_x.addWidget(self.listWidget_x)
        self.frame_y.addWidget(self.listWidget_y)

        self.gridLayout.addWidget(self.toolBar, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.frame_all, 2, 0, 4, 1)
        self.gridLayout.addWidget(self.pushButton_y, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_y, 3, 2, 1, 1)

        self.gridLayout.addWidget(self.variables_all, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.variables_y, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.variables_x, 4, 2, 1, 1)

        self.verticalLayout.addWidget(self.pushButton_all)
        self.verticalLayout.addWidget(self.pushButton_x)
        self.gridLayout.addLayout(self.verticalLayout, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_x, 5, 2, 1, 1)

        self.variables_all.setCheckable(False)
        self.variables_y.setCheckable(False)
        self.variables_x.setCheckable(False)

        self.listWidget_all.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_x.setSelectionMode(QAbstractItemView.ExtendedSelection)

        StyleSheet.GALLERY_INTERFACE.apply(self)

    def __initListWidgets(self):
        self.pushButton_x.setEnabled(False)
        self.pushButton_y.setEnabled(False)
        self.pushButton_all.setEnabled(False)

        self.resetLists()

    def __initButtons(self):
        self.pushButton_x.setEnabled(True)
        self.pushButton_y.setEnabled(True)
        self.pushButton_all.setEnabled(True)

        self.pushButton_x.setText(self.tr("Add"))
        self.pushButton_y.setText(self.tr("Add"))
        self.pushButton_all.setText(self.tr("Add all"))

        self.add_to_x = True
        self.add_to_y = True

    def enbaleAllButtons(self, enabled):
        self.pushButton_all.setEnabled(enabled)
        self.pushButton_x.setEnabled(enabled)
        self.pushButton_y.setEnabled(enabled)
        self.toolBar.compareButton.setEnabled(enabled)
        self.toolBar.calcaulateButton.setEnabled(enabled)
        self.toolBar.resetButton.setEnabled(enabled)

    def __initConnects(self):
        self.toolBar.resetButton.clicked.connect(self.resetLists)
        self.listWidget_all.clicked.connect(self.__initButtons)
        self.listWidget_x.clicked.connect(self.remove_from_x)
        self.listWidget_y.clicked.connect(self.remove_from_y)
        self.pushButton_x.clicked.connect(self.clicked_button_x)
        self.pushButton_y.clicked.connect(self.clicked_button_y)
        self.pushButton_all.clicked.connect(self.clicked_button_all)
        self.toolBar.calcaulateButton.clicked.connect(self.calculate)
        self.toolBar.compareButton.clicked.connect(self.compare)
        self.pkThread.finished_signal.connect(self.calculate_compare_finished)
        self.pkThread.error_signal.connect(self.error_occurred)
        self.pkThread.warn_signal.connect(self.warn_occurred)

    def resetLists(self):
        self.setList(self.listWidget_x, [])
        self.setList(self.listWidget_y, [])
        self.setList(self.listWidget_all, self.list_all)

    def setList(self, list_widget, list_content):
        while list_widget.count() > 0:
            list_widget.takeItem(0)
        for content in list_content:
            if not isinstance(content, str):
                content = str(content)
            list_widget.addItem(QListWidgetItem(content))
        list_widget.clearSelection()

    def updateList(self):
        df = get_value("current_workbook")
        self.list_all = df.columns
        self.resetLists()
        self.__initButtons()

        set_value("pk", None)
        set_value("pk_dict", {})
        set_value("pk_name_dict", {})
        set_value("pk_n", 0)

        set_value("pks", None)
        set_value("pks_dict", {})
        set_value("pks_name_dict", {})
        set_value("pks_n", 0)

        self.logger.info(self.tr("Update the available variables in the data. All the storage cache has been reset."))
        self.logger.info(self.tr("The available variables list as {0}").format(self.list_all))

    def remove_from_x(self):
        self.pushButton_x.setText(self.tr("Remove"))
        self.pushButton_all.setText(self.tr("Remove all"))
        self.add_to_x = False

    def remove_from_y(self):
        self.pushButton_y.setText(self.tr("Remove"))
        self.add_to_y = False

    def exchange_selected(self, source, destination):
        selected = source.selectedIndexes()
        idx = [x.row() for x in selected]
        idx.sort(reverse=True)
        for num in idx:
            it = source.takeItem(num)
            destination.addItem(it)
        source.clearSelection()
        destination.clearSelection()

    def remove_all(self, source, destination):
        while source.count() > 0 :
            it = source.takeItem(0)
            destination.addItem(it)

    def clicked_button_x(self):
        if self.add_to_x:
            self.exchange_selected(self.listWidget_all, self.listWidget_x)
        else:
            self.exchange_selected(self.listWidget_x, self.listWidget_all)

    def clicked_button_y(self):
        if self.add_to_y:
            if self.listWidget_y.count() == 0 and len(self.listWidget_all.selectedItems()) == 1:
                self.exchange_selected(self.listWidget_all, self.listWidget_y)
            else:
                pass
        else:
            self.exchange_selected(self.listWidget_y, self.listWidget_all)

    def clicked_button_all(self):
        if self.add_to_x:
            self.remove_all(self.listWidget_all, self.listWidget_x)
        else:
            self.remove_all(self.listWidget_x, self.listWidget_all)

    def collect_xy(self):
        x = []
        y = []
        n = self.listWidget_x.count()
        for i in range(n):
            x.append(self.listWidget_x.item(i).text())

        n = self.listWidget_y.count()
        for i in range(n):
            y.append(self.listWidget_y.item(i).text())

        set_value("x_names", x)
        set_value("y_names", y)
        set_value("output_dir", cfg.get(cfg.outputFolder))

        self.logger.info(self.tr("The test variables include the following:"))
        self.logger.info(x)
        self.logger.info(self.tr("The independent variable includes the following:"))
        self.logger.info(y)

    def calculate(self):
        self.logger.info(self.tr("Start calculating PKs."))
        self.toolBar.textButton.setText(self.tr("Calculating"))
        self.toolBar.showProgressBar(True)
        self.enbaleAllButtons(False)
        self.collect_xy()
        self.pkThread.set_work_type("PK")
        self.pkThread.start()
        self.calculate_started_signal.emit(self.tr("Calculating PKs"))

    def compare(self):
        self.logger.info(self.tr("Start comparing PKs."))
        self.toolBar.textButton.setText(self.tr("Comparing"))
        self.toolBar.showProgressBar(True)
        self.enbaleAllButtons(False)
        self.collect_xy()
        self.pkThread.set_work_type("PKC")
        self.pkThread.start()
        self.calculate_started_signal.emit(self.tr("Comparing PKs"))

    def calculate_compare_finished(self):
        self.toolBar.showProgressBar(False)
        self.enbaleAllButtons(True)
        self.toolBar.createTopRightInfoBar(self.tr("Success!"), self.tr("The operation success! Please refer the output for details."), InfoBar.success)
        self.calculate_finished_signal.emit(self.tr("Open the file {0}").format(get_value("last_work_file")))

    def error_occurred(self, str):
        self.toolBar.showProgressBar(False)
        self.enbaleAllButtons(True)
        self.toolBar.createTopRightInfoBar(self.tr("Error!"), str,InfoBar.error)

    def warn_occurred(self, str):
        self.toolBar.createTopRightInfoBar(self.tr("Warn!"), str,InfoBar.warning)


