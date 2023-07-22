# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from common.signal_bus import signalBus
from common.config import VERSION
from utils.logger import Logger
from view.home_interface import HomeInterface
from view.setting_interface import SettingInterface
from view.data_interface import DataInterface
from view.operate_interface import OperateInterface
from view.output_interface import  OutputInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)
        self.dataInterface = DataInterface(self)
        self.operateInterface = OperateInterface(self)
        self.outputInterface = OutputInterface(self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

        self.logger = Logger().get_logger()
        self.logger.info(self.tr("Init software {0} finished!").format(VERSION))

    def initLayout(self):
        self.dataInterface.toolBar.newDataReadSig.connect(self.operateInterface.updateList)
        self.operateInterface.pkThread.finished_signal.connect(self.outputInterface.updateData)
        self.operateInterface.pkThread.finished_signal.connect(self.outputInterface.toolBar.enable_buttons)
        self.operateInterface.calculate_started_signal.connect(self.outputInterface.toolBar.changeText)
        self.operateInterface.calculate_started_signal.connect(self.outputInterface.initTable)
        self.operateInterface.calculate_finished_signal.connect(self.outputInterface.toolBar.changeText)
        self.operateInterface.calculate_finished_signal.connect(self.outputInterface.toolBar.showInfoBar)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)
        pass

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.navigationInterface.addSeparator()
        #
        pos = NavigationItemPosition.SCROLL

        self.addSubInterface(self.dataInterface, FIF.DOCUMENT, self.tr("Data"), pos)
        self.addSubInterface(self.operateInterface, FIF.CALENDAR, self.tr("Operate"), pos)
        self.addSubInterface(self.outputInterface, FIF.VIEW, self.tr("Output"), pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget(self.tr('Jiang Feng'), './resource/images/haibara.jpg'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon('./resource/images/logo.png'))
        self.setWindowTitle(self.tr('PK4ADI Calculator'))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        w = MessageBox(
            self.tr('Contact author'),
            'silencejiang@zju.edu.cn',
            self
        )
        w.exec()

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = [self.dataInterface, self.operateInterface, self.outputInterface]
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
