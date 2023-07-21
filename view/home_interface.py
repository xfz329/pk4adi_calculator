# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from qfluentwidgets import ScrollArea

from components.sample_card import SampleCardView
from common.style_sheet import StyleSheet
from view.widget.banner_widget import BannerWidget

class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """ load samples """
        # basic input samples
        startView = SampleCardView(
            self.tr("Start using PK4ADI Calculator!"), self.view)
        startView.addSampleCard(
            icon="./resource/images/controls/DataGrid.png",
            title="Input",
            content=self.tr(
                "Set input"),
            routeKey="data_interface",
            index=0
        )
        startView.addSampleCard(
            icon="./resource/images/controls/MenuFlyout.png",
            title="Variables",
            content=self.tr(
                "Set variables"),
            routeKey="operate_interface",
            index=0
        )
        startView.addSampleCard(
            icon="./resource/images/controls/DataGrid.png",
            title="Output",
            content=self.tr(
                "Get output"),
            routeKey="output_interface",
            index=0
        )

        self.vBoxLayout.addWidget(startView)