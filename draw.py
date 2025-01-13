# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 16:21:13 2022

@author: edelcore

Draw_cavity_profile: is used to retrieve the coordinates of the
profile to draw
"""

import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5 import uic
from os.path import isdir, normpath
from subprocess import call as scall
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure as plt_figure
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, QSize
from functools import partial
import os
from PyQt5.QtGui import QPixmap, QIcon

from Draw_cavity_profile import Draw_cavity_profile
#from Set_cav_database import Set_cav_database

draw_i, QtBaseClass = uic.loadUiType('draw.ui')

class draw(QDialog, draw_i):
    def __init__(self, parent, IC_EG, l1, l2, CAV, path):
        super(draw, self).__init__(parent)
        QDialog.__init__(self)
        draw_i.__init__(self)
        self.setupUi(self)
        
        self.IC_EG=IC_EG
        self.l1=l1
        self.l2=l2
        self.CAV=CAV
        self.path=path
        
        self.label2 = QLabel(self)
        self.pixmap2 = QPixmap()
                
        try:
            x = Draw_cavity_profile('', self.IC_EG, 1)
            IC_coo = x.CAV_coo()
            IC_coo[:,0] = -IC_coo[:,0] + IC_coo[-1,0] 
            IC_coo[:,0] = np.flip(IC_coo[:,0])
            IC_coo[:,1] = np.flip(IC_coo[:,1])
        
            self.EC_EG = np.zeros((3,8))
            self.EC_EG[0,:] = self.CAV[0,:]
            self.EC_EG[0,7] = 16
            x = Draw_cavity_profile('', self.EC_EG, 1)
            EC_coo = x.CAV_coo()
            EC_coo[:,0] = EC_coo[:,0] + IC_coo[-1,0]
        
            CAV_coo = np.append(IC_coo, EC_coo, axis = 0)
            end = CAV_coo[-1,0]
            
            if l2 == 0:
                add = np.array([[end + self.l1, CAV_coo[-1,1]],
                                [end + self.l1, 0],
                                [0,0],
                                [CAV_coo[0,0], CAV_coo[0,1]]])
            else:
                add = np.array([[end + self.l2, CAV_coo[-1,1]],
                                [end + self.l2 + np.abs(self.CAV[0,5]-self.CAV[2,5]), CAV_coo[0,1]],
                                [end + self.l1, CAV_coo[0,1]],
                                [end + self.l1, 0],
                                [0,0],
                                [CAV_coo[0,0], CAV_coo[0,1]]])
            CAV_coo = np.append(CAV_coo, add, axis = 0)
            
            fig,ax = plt.subplots(1)
            ax.axis('off')
            plt.plot(CAV_coo[:,0], CAV_coo[:,1], color='r')
            l=''
            file=open(path+"\\fileDraw.txt",'w')
            for i in range(len(CAV_coo)):
                l+=str(CAV_coo[i,0])+','+str(CAV_coo[i,1])+'\n'
            file.write(l)
            file.close()
            plt.savefig(path+"\\fileDraw.png")
        except:
            self.warning_wdj('Something wrong during the cavity profile definition')
        try:
            self.pixmap2 = QPixmap(path+"\\fileDraw.png")
            self.label2.setPixmap(self.pixmap2)
            self.label2.adjustSize()
        except:
            self.warning_wdj('Something goes wrong during the cavity profile drawing')

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        
##############################################################################

    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass