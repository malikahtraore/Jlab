# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 16:35:35 2022

@author: edelcore
"""

from PyQt5.QtWidgets import QWidget, QDialog, QFileDialog
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QIcon
import os
from PyQt5.QtWidgets import QMessageBox, QLabel
import numpy as np
from os.path import normpath
from datetime import datetime

printui, QtBaseClass = uic.loadUiType('print.ui')

class printt(QDialog, printui):
    def __init__(self, parent, CAV, path, output_file):
        super(printt, self).__init__(parent)
        QWidget.__init__(self)
        printui.__init__(self)
        self.setupUi(self)

        self.pushButton_Save.clicked.connect(self.save)

        self.label=QLabel(self)
        self.label.setPixmap(QPixmap(path+'\\figProfile.png'))
        self.label.setGeometry(400, 400, 360, 180)
        self.label.setScaledContents(True)
        self.label.move(720, 230)
        
        self.label1=QLabel(self)
        self.label1.setPixmap(QPixmap(path+'\\fieldProfile.png'))
        self.label1.setGeometry(400, 400, 360, 180)
        self.label1.setScaledContents(True)
        self.label1.move(10,230)

        self.label2=QLabel(self)
        self.label2.setPixmap(QPixmap(path+'\\figTTF.png'))
        self.label2.setGeometry(400, 400, 360, 180)
        self.label2.setScaledContents(True)
        self.label2.move(360,230)
        
        self.nameIC=parent.nameIC
        self.nameEG1=parent.nameEG1
        self.nameEG2=parent.nameEG2
        self.param=parent.param
        self.p=parent.p
        self.output_file=output_file
        self.FF=parent.FF
        self.betaTTF=parent.betaTTF
        
        self.l_inner.setText('Inner = '+self.nameIC)
        self.l_leftEG.setText('Left EndGroup = '+self.nameEG1)
        self.l_rightEG.setText('Right EndGroup = '+self.nameEG2)
        self.l_frequency.setText('Frequency = '+str(round(self.param[0],3))+' [MHz]')
        self.l_rq.setText('R/Q = '+str(self.param[1])+' [Ohm]')
        self.l_QBCS.setText('Q BCS @ 2K = '+str(format(float(self.param[2]),'.1E')))
        self.L_Epkk.setText('Epeak/Eacc = '+str(self.param[3])+' [MV/m]')
        self.l_Hpkk.setText('Hpeak/Eacc = '+str(self.param[4])+' [mT/(MV/m)]')
#        self.l_FieldFlatness.setText('Field Flatness = '+str(round(self.param[5],2)))
        self.l_FieldFlatness.setText('Field Flatness = '+str(round(float(self.FF),4))+' [%]')
        #self.l_effectiveBeta.setText('Effective Beta = '+str(round(self.param[6],2))+' ('+str(self.param[7])+', '+str(self.param[8])+')')        
        self.l_effectiveBeta.setText('Effective Beta = '+str(round(self.betaTTF,2))+' ('+str(self.param[7])+', '+str(self.param[8])+')')

        self.l_fIC1.setText('Frequency = '+str(round(self.p[0,0],3))+' [MHz]')
        self.l_epIC1.setText('Epeak/Eacc = '+str(round(self.p[0,1]/10,2))+' [MV/m]')
        self.l_hpIC1.setText('Hpeak/Eacc = '+str(self.p[0,2])+' [mT/(MV/m)]')
        self.l_k.setText('k = '+str(round(self.p[0,3]*100,4))+' [%]')
        self.l_f2.setText('Frequency = '+str(round(self.p[1,0],3))+' [MHz]')
        self.l_ep2.setText('Epeak/Eacc = '+str(self.p[1,1])+' [MV/m]')
        self.l_hp2.setText('Hpeak/Eacc = '+str(self.p[1,2])+' [mT/(MV/m)]')
        self.l_TL1.setText('Tube Length = '+str(self.p[1,3])+' [mm]')
        if self.p[1,4]!=0:
            self.l_TIRIS1.setText('TubeIris = '+str(self.p[1,4])+ ' [mm]')
        else:
            self.l_TIRIS1.setText('')
        self.l_f3.setText('Frequency = '+str(round(self.p[2,0],3))+ ' [MHz]')
        self.l_ep3.setText('Epeak/Eacc = '+str(self.p[2,1])+' [MV/m]')
        self.l_hp3.setText('Hpeak/Eacc = '+str(self.p[2,2])+ ' [mT/(MV/m)]')
        self.l_TL2.setText('Tube Length = '+str(self.p[2,3])+' [mm]')
        if self.p[2,4]!=0:
            self.l_TIRIS2.setText('TubeIris = '+str(self.p[2,4])+' [mm]')
        else:
            self.l_TIRIS2.setText('')
            
        # IC
        a=np.zeros((7))
        a=CAV[2,0:7]
        ic=self.g2p(a)
        
        self.l_rirIC1.setText('Riris = '+str(ic[5])+ ' [mm]')
        self.l_LIC1.setText('L = '+str(ic[6])+' [mm]')
        self.l_alphaIC1.setText('alpha = '+str(round(ic[0]*180/np.pi,2))+' [deg]')
        self.l_RIC1.setText('R = '+str(ic[4]))
        self.l_rIC1.setText('r = '+str(ic[3]))
        self.l_dIC1.setText('d = '+str(ic[1])+' [mm]')
        self.l_DIC1.setText('D = '+str(a[4])+' [mm]')
        
        # EG1
        a=np.zeros((7))
        a=CAV[1,0:7]
        pc=self.g2p(a)
        
        self.l_rirEG1_l.setText('Riris = '+str(pc[5])+' [mm]')
        self.l_LEG1_l.setText('L = '+str(pc[6])+' [mm]')
        self.l_alphaEG1_l.setText('alpha = '+str(round(pc[0]*180/np.pi,2))+' [deg]')
        self.l_REG1_l.setText('R = '+str(pc[4]))
        self.l_rEG1_l.setText('r = '+str(pc[3]))
        self.l_dEG1_l.setText('d = '+str(pc[1])+' [mm]')

        a=np.zeros((7))
        a=CAV[0,0:7]
        ec=self.g2p(a)
        
        self.l_rirEG1_r.setText('Riris = '+str(ec[5])+' [mm]')
        self.l_LEG1_r.setText('L = '+str(ec[6])+' [mm]')
        self.l_alphaEG1_r.setText('alpha = '+str(round(ec[0]*180/np.pi,2))+' [deg]')
        self.l_REG1_r.setText('R = '+str(ec[4]))
        self.l_rEG1_r.setText('r = '+str(ec[3]))
        self.l_dEG1_r.setText('d = '+str(ec[1])+' [mm]')
        self.l_DEG1.setText('D = '+str(a[4])+' [mm]')   
        
        # EG2
        
        a=np.zeros((7))
        a=CAV[4,0:7]
        pc=self.g2p(a)
        
        self.l_rirEG2_l.setText('Riris = '+str(pc[5])+' [mm]')
        self.l_LEG2_l.setText('L = '+str(pc[6])+' [mm]')
        self.l_alphaEG2_l.setText('alpha = '+str(round(pc[0]*180/np.pi,2))+' [deg]')
        self.l_REG2_l.setText('R = '+str(pc[4]))
        self.l_rEG2_l.setText('r = '+str(pc[3]))
        self.l_dEG2_l.setText('d = '+str(pc[1])+' [mm]')

        a=np.zeros((7))
        a=CAV[3,0:7]
        ec=self.g2p(a)
        
        self.l_rirEG2_r.setText('Riris = '+str(ec[5])+' [mm]')
        self.l_LEG2_r.setText('L = '+str(ec[6])+' [mm]')
        self.l_alphaEG2_r.setText('alpha = '+str(round(ec[0]*180/np.pi,2))+' [deg]')
        self.l_REG2_r.setText('R = '+str(ec[4]))
        self.l_rEG2_r.setText('r = '+str(ec[3]))
        self.l_dEG2_r.setText('d = '+str(ec[1])+' [mm]')
        self.l_DEG2.setText('D = '+str(a[4])+' [mm]')
        
        self.l_time.setText(str(datetime.now()))
        
        # try:
        #     screen = QtWidgets.QApplication.primaryScreen()
        #     screenshot = screen.grabWindow( self.winId() )
        #     screenshot.save(self.output_file+'\\img.jpg', 'jpg')
        # except:
        #     self.warning_wdj('Some errors occur saving the file in the outp_file folder')
            
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
        
##############################################################################
    
    def save(self):
        self.frame_save.hide()
        
        try:
            path, _ = QFileDialog.getSaveFileName(self,"Save file", self.output_file, "Image (*.jpg)")
            path = normpath(str(path)) 
            ok = 1
        except :
            ok = 0
        if ok ==1:
            screen = QtWidgets.QApplication.primaryScreen()
            screenshot = screen.grabWindow( self.winId() )
            #screenshot.save('C:\\Users\edelcore\Desktop\shot.jpg', 'jpg')
            screenshot.save(path, 'jpg')
            #self.unsetCursor()

##############################################################################

    def g2p(self, cav):
        phy = np.zeros((7))
        array = np.zeros((7))
        try:
            phy[0] = float(cav[0])
            phy[1] = float(cav[1])
            phy[2] = float(cav[2])
            phy[3] = float(cav[3])
            phy[4] = float(cav[4])
            phy[5] = float(cav[5])
            phy[6] = float(cav[6])
            if np.all(phy > 0):
                try: 
                    XYP = self.racc_point(phy)
                    A = phy[0]
                    B = phy[1]
                    a = phy[2]
                    b = phy[3]
                    R_eq = phy[4]
                    R_ir = phy[5]       
                    L = phy[6]
                    r = b/a
                    R = B/A
                    H = (R_eq-B)-(R_ir+b)
                    alpha = np.arctan2(XYP[1,0]-XYP[0,0],XYP[0,1]-XYP[1,1])
                    m = (XYP[0,1]-XYP[1,1])/(XYP[0,0]-XYP[1,0])
                    d = L - (R_ir-XYP[1,1])/m - XYP[1,0] 
                    
                    array[0]=round(alpha,4)
                    array[1]=round(d,4)
                    array[2]=round(H,4)
                    array[3]=round(r,4)
                    array[4]=round(R,4)
                    array[5]=round(R_ir,4)
                    array[6]=round(L,4)
                    # self.le_alpha.setText(str(round(alpha,self.round_val)))
                    # self.le_d.setText(str(round(d,self.round_val)))
                    # self.le_H.setText(str(round(H,self.round_val)))
                    # self.le_r.setText(str(round(r,self.round_val)))
                    # self.le_R.setText(str(round(R,self.round_val)))
                    # self.le_IRpy.setText(str(round(R_ir,self.round_val)))
                    # self.le_SLpy.setText(str(round(L,self.round_val)))
                except:
                    self.valueError()
                
            else:
                self.warning_float()
        except:
            self.warning_float()
            
        return array

##############################################################################
    
    def valueError(self):
        reply = QMessageBox.warning(
        self, "Message",
        "Value error: check carefully the input parameters.",
        QMessageBox.Ok)

        if reply == QMessageBox.Ok: 
            pass

##############################################################################
        
    def warning_float(self):
        reply = QMessageBox.warning(
        self, "Warning",
        "All cell parameters must be a positive float number.",
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass    
        
##############################################################################
        
    def racc_point(self, cell_data):
        a = cell_data[0]
        b = cell_data[1]
        A = cell_data[2]
        B = cell_data[3]
        d_eq = cell_data[4]
        D_ir = cell_data[5]
        L = cell_data[6]
        
        x0 = 0.0
        y0 = d_eq-b
        X0 = L
        Y0 = B+D_ir
        
        t1 = np.pi+0.001
        Xp = A*np.cos(t1)+X0
        Yp = B*np.sin(t1)+Y0
        am = a**2-(Xp-x0)**2
        bm = (Xp-x0)*(Yp-y0)
        cm = b**2-(Yp-y0)**2
        m1 = (-bm-np.sqrt(bm**2-am*cm))/am
        m2 = (-bm+np.sqrt(bm**2-am*cm))/am
        m = np.min(np.array([m1,m2]))
        res_a = m+B**2*(Xp-X0)/(A**2*(Yp-Y0))
        
        t2 = 3*np.pi/2-0.001
        Xp = A*np.cos(t2)+X0
        Yp = B*np.sin(t2)+Y0
        am = a**2-(Xp-x0)**2
        bm = (Xp-x0)*(Yp-y0)
        cm = b**2-(Yp-y0)**2
        m1 = (-bm-np.sqrt(bm**2-am*cm))/am
        m2 = (-bm+np.sqrt(bm**2-am*cm))/am
        m = np.min(np.array([m1,m2]))
        
        n = 0
        toll = 10
        while toll > 1e-5 and n < 100:
            t3 = (t1+t2)/2
            xP2 = A*np.cos(t3)+X0
            yP2 = B*np.sin(t3)+Y0
            am = a**2-(xP2-x0)**2
            bm = (xP2-x0)*(yP2-y0)
            cm = b**2-(yP2-y0)**2
            m1 = (-bm-np.sqrt(bm**2-am*cm))/am
            m2 = (-bm+np.sqrt(bm**2-am*cm))/am
            m = np.min(np.array([m1,m2]))
            res_c = m+B**2*(xP2-X0)/(A**2*(yP2-Y0))
            toll = np.abs(res_c)
            if toll < 1e-5:
                break
            elif np.sign(res_c) == np.sign(res_a):
                t1 = t3
            else:
                t2 = t3
            n = n+1
        
        ael = (b/a)**2+m**2
        bel = (-2)*((b/a)**2*x0+m**2*xP2-m*yP2+m*y0)
        xP1 = -bel*0.5/ael
        yP1 = m*(xP1-xP2)+yP2
        point = np.array([[xP1,yP1],[xP2,yP2]])
    
        return point 
    