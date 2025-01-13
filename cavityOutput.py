# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:18:21 2022

@author: edelcore

Defines the functions used to fill the cavity output window:
    - plot the transit time factor based on betamin and betamax
    defined by the user and retrieve the effective beta
    - plot the field data and compute the field flatness
    - replot the cavity profile
    - after the TTF computation, enable the print button to show
    the summary of the simulations
"""

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
import os
import re
import math
from PyQt5.QtWidgets import QMessageBox, QLabel
import numpy as np
from printt import printt
from os import remove, rename
from subprocess import call as scall
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


cavityOutputui, QtBaseClass = uic.loadUiType('CavityOutput.ui')

class cavityOutput(QDialog, cavityOutputui):
    def __init__(self, parent, CAV, path, peaks, output_file):
        super(cavityOutput, self).__init__(parent)
        QWidget.__init__(self)
        cavityOutputui.__init__(self)
        self.setupUi(self)
        
        self.nameIC=parent.nameIC
        self.nameEG1=parent.nameEG1
        self.nameEG2=parent.nameEG2
        self.param=np.zeros((9))
        self.betaeff=0
        self.p=parent.p
        self.output_file=output_file
        
        self.pb_Print.setEnabled(False)
        self.pb_Print.clicked.connect(self.click_print)
        self.pb_Quit.clicked.connect(self.click_quit)
        
        #self.pb_Replot.setEnabled(False)
        self.pb_Replot.clicked.connect(self.click_replot)
                
        self.pb_TTF.setEnabled(False)
        self.pb_TTF.clicked.connect(self.click_TTF)
        
        self.peaks=peaks
        self.CAV=CAV
        
        self.label4=QLabel(self)
        self.pixmap2 = QPixmap()

        self.path=path
        self.label2=QLabel(self)
        self.label2.setPixmap(QPixmap(self.path+'\\figProfile.png'))
        self.label2.setGeometry(400, 400, 390, 191)
        self.label2.setScaledContents(True)
        self.label2.move(580, 360)
        
        self.label3=QLabel(self)
        self.label3.setPixmap(QPixmap(self.path+'\\fieldProfile.png'))
        self.label3.setGeometry(400, 400, 390, 291)
        self.label3.setScaledContents(True)
        self.label3.move(580,40)
        
        self.betaTTF=0
        ## field flatness
        self.FF=0
        try:
            print('try')
            somma=0
            self.n=CAV[0,7]
            for i in range(len(self.peaks)):
                somma=somma+self.peaks[i]
            # CERN way to compute FF
            self.FF=100-(np.max(self.peaks)-np.min(self.peaks))*100/(somma/self.n)
            a=''
            for i in range(len(self.peaks)):
               a+='Cell '+str(i+1)+': '+str(self.peaks[i])+'\n'
               
            # LASA way to compute FF: I use this one
            self.FF=100-(1-np.min(self.peaks)/np.max(self.peaks))*100

            self.te_peaks.setText(a)
            self.label.setText('Flatness: '+str(round(self.FF,4))+'%')
        except:
            self.warning_wdj('Some errors occur in the Field Flatness calculation')
        
        self.fill_elmg_param()

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        
##############################################################################

    def click_quit(self):
        self.close()

##############################################################################
    
    def click_print(self):
        widget=printt(self, self.CAV, self.path, self.output_file)
        widget.exec()
        
        
##############################################################################

    def click_replot(self):
        minS=self.tE_minBeta.text()
        maxS=self.tE_maxBeta.text()
        phiS=self.tE_phii.text()
        m=0
        n=0
        o=0
        try:
            minN=float(minS)
        except:
            m=1
        try:
            maxN=float(maxS)
        except:
            n=1
        try:
            phiN=float(phiS)
        except:
            o=1
        
        if m==1 or n==1 or o==1:
            if m==1:
                self.warning_wdj("Please insert a valid number for min beta in range")
            elif n==1:
                self.warning_wdj("Please insert a valid number for max beta in range")
            elif o==1:
                self.warning_wdj("Please insert a valid number for synchronous phase")
            self.pb_TTF.setEnabled(False)
        else:
            if minN<0 or minN>1:
                self.warning_wdj('Please insert a valid number for min beta in range')
            elif maxN<0 or maxN>1:
                self.warning_wdj('Please insert a valid number for max beta in range')
            elif phiN<0 or phiN>180:
                self.warning_wdj('Please insert a valid number for synchronous phase')
            else:
                testo=self.l_TTF.text()
                if testo.__contains__('Enter'):
                    self.pb_TTF.setEnabled(True)
                    self.l_TTF.setText('')
                else:
                    self.click_TTF()
                    

        
##############################################################################

    def click_TTF(self):
        nbeta=100
        try:
            betamin=float(self.tE_minBeta.text())
        except:
            if(self.tE_minBeta.text()==''):
                self.warning_wdj("Min beta in range cannot be empty")
        try:
            betamax=float(self.tE_maxBeta.text())
        except:
            if self.tE_maxBeta.text()=='':
                self.warning_wdj('Max beta in range cannot be empty')
        try:
            phii=float(self.tE_phii.text())
        except:
            if self.tE_phii.text()=='':
                self.warning_wdj('Synchronous Phase cannot be empty')
        ncell=int(self.n)
        beta=np.zeros((104))
        for i in range(nbeta):
          beta[i + 1] = betamin + i * (betamax - betamin) / (nbeta - 1)

        self.betaeff = beta[1]
        self.param[7]=round(betamin,4)
        self.param[8]=round(betamax,4)
        self.def_beta_optim()
        #s='Effective beta for this cavity is = '+str(round(self.betaeff,4))+' ('+str(round(beta[2],4))+'-'+str(round(beta[3],4))+')'
        
        
        self.pb_Print.setEnabled(True)
        
        #### TBL
        
        file=open(self.path+'\\elmg_file\\AF_file.AF','r')
        line=file.readlines()
        file.close()
        beta1=betamin
        beta2=betamax
        s=str('ibeta=1, beta1='+str(beta1)+', beta2='+str(beta2)+' dbeta=0.005, \n')
        for i in range(len(line)):
            if line[i].__contains__('beta'):
                a=line[i].replace('\n',s)
        file=open(self.path+'\\elmg_file\\AF_file.AF','w')
        for i in range(len(line)):
            if i==12:
                file.writelines(a)
            else:
                file.writelines(line[i])
        file.close()
        scall(self.path+'\\elmg_file\\AF_file.AF', shell=True) 
        
        ####
        
        file=open(self.path+'\\elmg_file\\TBETA.TBL','r')
        line=file.readlines()
        file.close()
        
        x=[]
        y=[]
        z=[]
        delta=[]
        i1=0
        i2=0
        for i in range(len(line)):
            t=re.sub('\\s+',';',line[i])
            s=t.split(';')
            if line[i].__contains__('Beta') and line[i].__contains__('Zc'):
                i1=i
            elif line[i].__contains__('EndData'):
                i2=i
        for i in range(i1+2,i2):
                t=re.sub('\\s+',';',line[i])
                s=t.split(';')
                x.append(float(s[0]))
                y.append(float(s[3]))
                z.append(float(s[6]))

        for i in range(len(x)):
            delta.append(y[i]-np.tan(float(math.pi/180*phii))*z[i])
            
        plt.figure()
        plt.plot(x, delta, color='red')
        plt.grid()
        plt.xlabel(r'$\beta$')
        plt.ylabel('TTF')
        plt.savefig(self.path+'\\figTTF.png')
        betaTTF=0
        for i in range(0,len(x)):
            if delta[i]==np.max(delta):
                betaTTF=x[i]
        self.betaTTF=betaTTF
        
        #s='Effective beta for this cavity is = '+str(round(self.def_beta_optim(),2))+' ('+str(round(beta[2],4))+'-'+str(round(beta[3],4))+')'
        s='Effective beta for this cavity is = '+str(round(self.betaTTF,2))+' ('+str(round(beta1,2))+'-'+str(round(beta2,2))+')'        
        self.l_TTF.setText(s)
        
        self.pixmap2 = QPixmap(self.path+'\\figTTF.png')
        self.label4.setPixmap(self.pixmap2)
        self.label4.setGeometry(400, 400, 510, 280)
        self.label4.setScaledContents(True)
        self.label4.move(20, 340)
        self.show() 
        
##############################################################################        
           
    def elmg_axis_field(self):
        try:
            sfo_file  = open(self.path + '\\elmg_file\\AF_FILE.SFO', 'r')
            cont = sfo_file.readlines()
            for k in range(len(cont)-1,0,-1):
                if str([x for x in cont[k].split(' ') if x][0]) == 'ZLONG':
                    L = float([x for x in cont[k].split(' ') if x][1])
                    break
            sfo_file.close()
                       
            af_new =  open(self.path + '\\elmg_file\\AF_FILE.IN7', 'w')
            cont_af = ['line	plotfiles\n', 
                      '0.0 0.0 ' + str(L) + ' 0.0\n',
                      '200\n',
                      'end']
            af_new.writelines(cont_af)
            af_new.close()
             
            scall(self.path + '\\elmg_file\\AF_FILE.IN7', shell=True)
            try:
                remove(self.path + '\\elmg_file\\AF_FILE_axis.TBL')
            except:
                pass
            rename(self.path + '\\elmg_file\\AF_FIL01.TBL',  self.path + '\\elmg_file\\AF_FILE_axis.TBL')
            
            self.field_data()
            
        except:
            self.critical_wdj = ('Error reading AF_FILE.SFO file.')
            
##############################################################################
        
    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass 
 
##############################################################################
    
    def fill_elmg_param(self):
        sfo_file  = open(self.path+'\\elmg_file\\AF_file.SFO', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        
        self.SF_param = [0]*9
        f_pi = self.Resonance_frequency()
        
        for k in range(len(cont)-1,0,-1):
            line = [x for x in cont[k].strip().split(' ') if x]
            try:
                if line[0] == 'Frequency':
                    self.SF_param[0] = str(f_pi)
                    self.SF_param[1] = line[-1]
                    break
                elif line[0] == 'Q':
                    self.SF_param[2] = line[2]
                elif line[0] == 'r/Q':
                    self.SF_param[3] = line[2]
                    self.SF_param[4] = line[3]
                if line[0] == 'Maximum' and line[1] == 'E': 
                    self.SF_param[5] = line[-4]          
                    line2 = [x for x in cont[k-1].strip().split(' ') if x]
                    self.SF_param[6] = line2[-4]  
            except:
                pass

        #self.le_f.setText(self.SF_param[0])
        self.l_freq.setText('Frequency = ' + str(round(float(self.SF_param[0]),4))+' [MHz]')           
        self.l_RQ.setText('r/Q = ' + str(round(float(self.SF_param[3]),4)) + ' [Ohm]') 
        self.l_QBCS.setText('Q BCS factor @ 2K = ' + str(format(float(self.SF_param[2]),'.1E')))
        E_peak = float(self.SF_param[5])
        self.l_Epkk.setText('Epeak/Eacc = ' + str(round(E_peak/10, 4))) 
        H_peak = float(self.SF_param[6]) * 0.0012566370614359172
        self.l_Hpkk.setText('Hpeak/Eacc = ' + str(round(H_peak/10,4))) 
        
        self.param[0]=round(float(self.SF_param[0]),4)
        self.param[1]=round(float(self.SF_param[3]),4)
        self.param[2]=format(float(self.SF_param[2]),'.1E')
        self.param[3]=round(E_peak/10,4)
        self.param[4]=round(H_peak/10,4)
        self.param[5]=self.FF
        self.def_beta_optim()
        self.param[6]=self.beta
        
############################################################################## 
    
    def Resonance_frequency(self):
        sfo_file  = open(self.path+'\\elmg_file\\OUTFIS.TXT', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        for k in range(len(cont)-1,0,-1):
            if str([x for x in cont[k].split(' ') if x][0]) == 'FREQ':
                F_resonance = float([x for x in cont[k].split(' ') if x][1])
                break
    
        return F_resonance 

############################################################################### 

    def def_beta_optim(self):
        file  = open(self.path+'\\elmg_file\\AF_file.AF', 'r')
        testo = file.readlines()
        file.close()       

        save_l_ch = testo[12]
        l_ch = [x for x in testo[12].split(',') if x]
        l_ch = l_ch[0:-1] + ['IBETA = 1, BETA1 = 0.5, BETA2 = 0.99, DBETA = 0.01\n'] #BETA2 before = 0.8
        testo[12] = ','.join(l_ch)
        
        file  = open(self.path+'\\elmg_file\\AF_file.AF', 'w')
        file.write(''.join(testo))
        file.close()

        scall(self.path+'\\elmg_file\\AF_file.AF', shell=True)

        file  = open(self.path+'\\elmg_file\\AF_file.AF', 'r')
        testo = file.readlines()
        file.close()        

        testo[12] = save_l_ch
        
        file  = open(self.path+'\\elmg_file\\AF_file.AF', 'w')
        file.write(''.join(testo))
        file.close()

        file  = open(self.path+'\\elmg_file\\TBETA.TBL', 'r')
        res = file.readlines()
        file.close()

        beta = []
        T = []
        for k in range(len(res)):
            try:
                beta += [float([x for x in res[k].split(' ') if x][0])]
                T += [float([x for x in res[k].split(' ') if x][3])]
            except:
                pass

        f = CubicSpline(beta, T)
        df = CubicSpline.derivative(f, 1)

        #b_p_int = np.linspace(0.5,0.8, 1000)
        b_p_int = np.linspace(0.5,0.99, 1000)
        indx = np.where(f(b_p_int) == f(b_p_int).max())[0][0]
        
        toll = 1e-8
        err = 1
        x1 = b_p_int[indx-1]
        #### NON SO SE E' GIUSTO
        try:
            x2 = b_p_int[indx+1]
        except:
            x1 = b_p_int[indx-2]
            x2 = b_p_int[indx]
        #### altrimenti era solo row 405    
        
        cont=0
        den=2
        while err > toll and cont<10000:
            cont+=1
            ### riga da mettere nel caso al posto di 416, NON SO SE E' GIUSTA RIGA 416
            x3 = (x1 + x2) * 0.5
            #x3 = np.sqrt((x1**2+x2**2)/2)
           # if cont>20:
            #    den+=1
             #   x3 = np.sqrt((x1**2+x2**2)/den)

            if df(x3) > 0 and df(x1) < 0:
                x2 = x3
            elif df(x3) > 0 and df(x2) < 0:
                x1 = x3
            elif df(x3) < 0 and df(x1) > 0:
                x2 = x3
            if df(x3) < 0 and df(x2) > 0:
                x1 = x3
            err = df(x3)
        if cont==10000:
            self.beta=0.99
        else:
            self.beta = x3
        
        
        af_old =  open(self.path+'\\elmg_file\\AF_file.AF', 'r')
        cont_af = af_old.readlines()
        af_old.close()
        af_new =  open(self.path+'\\elmg_file\\AF_file.AF', 'w')                
        cont_af_del = [x for x in cont_af[12].split(',') if x] 
        cont_af[12] = 'beta=' + str(self.beta) + ',' + cont_af_del[1] + ',' + cont_af_del[2] + ',\n'
        af_new.writelines(cont_af)
        af_new.close()
        
        return self.beta