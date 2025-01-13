# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 13:25:49 2022

@author: edelcore
"""

import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5 import uic
from os.path import isdir, normpath
from subprocess import call as scall
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure as plt_figure
from PyQt5.QtCore import Qt, QSize
from functools import partial
import os
from PyQt5.QtGui import QPixmap, QIcon
import matplotlib.pyplot as plt


Ui_variableParam, QtBaseClass = uic.loadUiType('variableParam.ui')

class variableParam(QDialog, Ui_variableParam):
    def __init__(self, parent):
        super(variableParam, self).__init__(parent)
        QDialog.__init__(self)
        Ui_variableParam.__init__(self)
        self.setupUi(self)
        
##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)