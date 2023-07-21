#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   demo.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import os
import sys
from qfluentwidgets import FluentTranslator

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication

import globalvar.vars as gl
from common.config import cfg
from view.main_window import MainWindow

# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# internationalization
locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "gallery", ".", "./resource/i18n")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)

gl.init_()

# create main window
w = MainWindow()
w.show()

app.exec_()