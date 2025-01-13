# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 16:57:43 2022

@author: edelcore
"""

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
import os


infoui, QtBaseClass = uic.loadUiType('info_Tube.ui')

class info_Tube(QDialog, infoui):
    def __init__(self, parent):
        super(info_Tube, self).__init__(parent)
        QWidget.__init__(self)
        infoui.__init__(self)
        self.setupUi(self)
        
##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)