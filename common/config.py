# coding:utf-8
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, EnumSerializer, FolderValidator, ConfigSerializer, __version__)


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """ Config of application """

    # folders
    outputFolder = ConfigItem(
        "Folders", "Output", "output", FolderValidator())

    # main window
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # software update
    # checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


YEAR = "2004-2020"
AUTHOR = "Jiang Feng"
VERSION = "0.1.4"
HELP_URL = "https://xfz329-pk4adi-tutorial.readthedocs.io/en/latest/"
REPO_URL = "https://github.com/xfz329/pk4adi_gui"
FEEDBACK_URL = "https://github.com/xfz329/pk4adi_gui/issues"
RELEASE_URL = "https://github.com/xfz329/pk4adi_gui/releases"
CITE_URL = "https://www.zju.edu.cn"
UI_URL = "https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/"
KERNEL_URL = "https://github.com/xfz329/pk4adi"

cfg = Config()
qconfig.load('config/config.json', cfg)