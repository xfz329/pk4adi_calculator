# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, MessageBox

from common.config import cfg, HELP_URL, FEEDBACK_URL, UI_URL, KERNEL_URL, VERSION, YEAR, KERNEL_VERSION
from common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """ Setting interface """

    # checkUpdateSig = pyqtSignal()
    outputFolderChanged = pyqtSignal(str)
    minimizeToTrayChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Settings"), self)

        # output folders
        self.outputFolderGroup = SettingCardGroup(
            self.tr("Directory"), self.scrollWidget)
        self.outputFolderCard = PushSettingCard(
            self.tr('Choose directory'),
            FIF.DOWNLOAD,
            self.tr("Root Output directory"),
            cfg.get(cfg.outputFolder),
            self.outputFolderGroup
        )

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )

        # update software
        # self.updateSoftwareGroup = SettingCardGroup(
        #     self.tr("Software update"), self.scrollWidget)
        # self.updateOnStartUpCard = SwitchSettingCard(
        #     FIF.UPDATE,
        #     self.tr('Check for updates when the application starts'),
        #     self.tr('The new version will be more stable and have more features'),
        #     configItem=cfg.checkUpdateAtStartUp,
        #     parent=self.updateSoftwareGroup
        # )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('Open help page'),
            FIF.HELP,
            self.tr('Help'),
            self.tr(
                'Discover new features and learn useful tips about PK4ADI Calculator'),
            self.aboutGroup
        )
        self.uiCard = HyperlinkCard(
            UI_URL,
            self.tr('Open help page'),
            FIF.APPLICATION,
            self.tr('UI'),
            self.tr(
                'Based on PyQt-Fluent-Widgets developed by zhiyiYo'),
            self.aboutGroup
        )
        self.kernelCard = HyperlinkCard(
            KERNEL_URL,
            self.tr('Open home page'),
            FIF.INFO,
            self.tr('Kernel'),
            self.tr(
                'Based on python package PK4ADI ') + KERNEL_VERSION,
            self.aboutGroup
        )
        self.licenseCard = PrimaryPushSettingCard(
            self.tr('Show license'),
            FIF.DICTIONARY,
            self.tr('License'),
            self.tr('MIT'),
            self.aboutGroup
        )
        self.authorsCard = PrimaryPushSettingCard(
            self.tr('Show authors'),
            FIF.PEOPLE,
            self.tr('Authors'),
            '© ' + self.tr('Copyright') + f" {YEAR}" +self.tr(", ")+self.tr("Zhejiang University. ") +
            self.tr('Version') + " " + VERSION,
            self.aboutGroup
        )
        self.acknowledgementCard = PrimaryPushSettingCard(
            self.tr('Show contributors'),
            FIF.PEOPLE,
            self.tr('Acknowledgement'),
            self.tr('Thank the contributors of the software'),
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('Provide feedback'),
            FIF.FEEDBACK,
            self.tr('Provide feedback'),
            self.tr('Help us improve PK4ADI Calculator by providing feedback'),
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.outputFolderGroup.addSettingCard(self.outputFolderCard)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.personalGroup.addSettingCard(self.languageCard)

        # self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.uiCard)
        self.aboutGroup.addSettingCard(self.kernelCard)
        self.aboutGroup.addSettingCard(self.licenseCard)
        self.aboutGroup.addSettingCard(self.authorsCard)
        self.aboutGroup.addSettingCard(self.acknowledgementCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.outputFolderGroup)
        self.expandLayout.addWidget(self.personalGroup)
        # self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )

    def __onOutputFolderCardClicked(self):
        """ output folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.outputFolder) == folder:
            return

        cfg.set(cfg.outputFolder, folder)
        self.outputFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(setTheme)

        # output folder
        self.outputFolderCard.clicked.connect(
            self.__onOutputFolderCardClicked)

        # personalization
        self.themeColorCard.colorChanged.connect(setThemeColor)

        # about
        self.licenseCard.clicked.connect(self.show_license)
        self.authorsCard.clicked.connect(self.show_authors)
        self.acknowledgementCard.clicked.connect(self.show_contributors)

        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))

    def show_authors(self):
        w = MessageBox(
            self.tr("Authors"),
            self.tr("College of Biomedical Engineering & Instrument Science, Zhejiang University") + "\n"
            + self.tr("Prof. Hang Chen") + "\n"
            + self.tr("Feng Jiang") + "\n"
            + self.tr("Mengge Zhang") + "\n"
            + self.tr("Wanlin Chen") + "\n"
            + self.tr("Women's Hospital, School of Medicine, Zhejiang University") + "\n"
            + self.tr("Prof. Xinzhong Chen") + "\n"
            + self.tr("Hua Li"),
            self
        )
        w.exec()

    def show_license(self):
        w = MessageBox(
            self.tr('License'),
            "The MIT License (MIT) \n"
            "Copyright (c) 2023 Zhejiang University.\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy "
            "of this software and associated documentation files (the \"Software\"), to deal "
            "in the Software without restriction, including without limitation the rights "
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
            "copies of the Software, and to permit persons to whom the Software is "
            "furnished to do so, subject to the following conditions:\n"
            "The above copyright notice and this permission notice shall be included in all "
            "copies or substantial portions of the Software.\n"
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
            "SOFTWARE.",
            self
        )
        w.exec()

    def show_contributors(self):
        w = MessageBox(
            self.tr('Contributors'),
            "Warren D.Smith\n"
            "Robert C.Dutton\n"
            "Ty N.Smith\n"
            "zhiyiYo",
            self
        )
        w.exec()
