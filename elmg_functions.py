# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 09:35:47 2022

@author: edelcore
"""

from os import remove, listdir
from os.path import isdir, join, getsize, normpath
import numpy as np
from subprocess import call as scall
from scipy.interpolate import CubicSpline
from shutil import rmtree, copyfile
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from Draw_cavity_profile import Draw_cavity_profile
from geometry import Geometry
from electromagnetic_functions import emfn

Ui_EG_tune, QtBaseClass = uic.loadUiType('EG_tune.ui')

class elmg_functions():
    def __init__(self, path, CAV, F_guess, dx, beta):
        self.path = path
        #self.elmg_param = elmg_param
        self.Eacc = 10
        self.dx = CAV[0,4]/50
        self.temp_type = 2 # T = 2K
        self.beta_type = 1 # beta geom
        self.part_acc = 1 # = 1 proton, else = 2
        self.path_to_elmg_file=path
        
        self.MATP = np.array([8.57E-6, 1.06E+5, 1.18E+5, 0.4, 0.38, 50, 1.52e-05, 0, 0.00146])

        self.CAV = CAV
        
        self.elmg_param=np.zeros(25)
        self.elmg_param[22]=-2
        self.beta=0
        self.round_val = 2
        self.SF_param=[0]*9
        
##############################################################################
# Write SuperFish file and run simulation for EG
    def run_EG_sym_f(self, path, CAV, F_guess, dx, beta):
       
        CAV[0,7] = 18
        x = Draw_cavity_profile(path, CAV, 1.4)  
        geom = Geometry()  
        IC = CAV[2,0:7]
        Pic = geom.racc_point(CAV[2,0:7])
        #Pic = x.racc_point(CAV[2,0:7])
        CAV[0,7] = 16
        x = Draw_cavity_profile(path, CAV, 1.4)   
        EC = CAV[0,0:7]
        Pec = geom.racc_point(CAV[0,0:7])
        #Pec = x.racc_point(CAV[0,0:7])
        
        l_tube = CAV[1,7]
        l_tube_Rir = CAV[2,7]
                 
        lines = [
        'Simulation file:',
        ' ',   
        '$reg kprob=1, conv = 0.1,',
        'dx=' + str(dx) + ', freq=' + str(F_guess) + ',',
        'xdri= ' + str(IC[6]) + ', ydri=' + str(IC[4] - dx) + ',',
        'nbslf=0, nbsrt=1, dslope =-1,',
        'beta=' + str(beta) + ', rmass = -2, kmethod=1, ',
        'irtype=1, tempk=2.0, tc=9.2, residr=0.0,',
        'clength=' + str(IC[6]+EC[6]) + ', zctr=' + str(IC[6]) + ', norm=1 , EZEROT = 10000000$ \n',
        ' ']  
        
        X_c = [0]
        lines += [
        '$po x=0.0, y=0.0$',
        '$po x=0.0, y='+str(IC[5])+'$',
        '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[5]+IC[3])+', x='+str(IC[6]-Pic[1,0])+', y='+str(Pic[1,1]-(IC[5]+IC[3]))+', A='+str(IC[2])+', B='+str(IC[3])+'$',
        '$po x='+str(X_c[-1]+IC[6]-Pic[0,0])+ ', y ='+str(Pic[0,1])+ '$',
        '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[4]-IC[1])+', x= 0.0, y='+str(IC[1])+', A='+str(IC[0])+', B='+str(IC[1])+'$']
        
        X_c += [IC[6]]
        
        lines += [
        '$po NT=2, x0='+str(X_c[-1])+', y0='+str(EC[4]-EC[1])+', x='+str(Pec[0,0])+', y='+str(Pec[0,1]-(EC[4]-EC[1]))+', A='+str(EC[0])+', B='+str(EC[1])+'$',
        '$po x='+str(X_c[-1]+Pec[1,0])+ ', y ='+str(Pec[1,1])+ '$',
        '$po NT=2, x0='+str(X_c[-1]+EC[6])+', y0='+str(EC[5]+EC[3])+', x=0.0, y='+str(-EC[3])+', A='+str(EC[2])+', B='+str(EC[3])+'$',] 
        
        X_c += [X_c[-1]+EC[6]]
         
        if l_tube_Rir == 0:
            X_c += [X_c[-1]+l_tube]
            lines += ['$po x='+str(X_c[-1])+', y='+str(EC[5])+ '$',
            '$po x='+str(X_c[-1])+', y=0.0$',
            '$po x=0.0, y=0.0$']  
        else:
            X_c += [X_c[-1]+l_tube_Rir]
            lines += ['$po x='+str(X_c[-1])+', y='+str(EC[5])+ '$']
            X_c += [X_c[-1] + np.abs(CAV[0,5]-CAV[2,5])]          
            lines += ['$po x='+str(X_c[-1])+', y='+str(IC[5])+ '$']            
            X_c += [IC[6] + EC[6] + l_tube]  
            lines += ['$po x='+str(X_c[-1])+', y='+str(IC[5])+ '$', 
            '$po x='+str(X_c[-1])+', y=0.0$',
            '$po x=0.0, y=0.0$']  
               
        af_file =  open(path + '\\elmg_file\\AF_file.AF', 'w')           
        af_file.write('\n'.join(lines))
        af_file.close()
        
        scall(path+'\\elmg_file\\AF_file.AF', shell=True)
        
##############################################################################                    
                          
    def fill_elmg_parameters_f(self, CAV):
        sfo_file  = open(self.path_to_elmg_file+'\\elmg_file\\AF_file.SFO', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        
        self.SF_param = [0]*9
        emfn=emfn()
        f_pi = emfn.Resonance_frequency(self.path_to_elmg_file)
        #f_pi = self.Resonance_frequency(self.path_to_elmg_file)

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
        return self.SF_param

############################################################################## 
    
    # def Resonance_frequency(self, path):
    #     sfo_file  = open(path+'\\elmg_file\\OUTFIS.TXT', 'r')
    #     cont = sfo_file.readlines()
    #     sfo_file.close()
    #     for k in range(len(cont)-1,0,-1):
    #         if str([x for x in cont[k].split(' ') if x][0]) == 'FREQ':
    #             F_resonance = float([x for x in cont[k].split(' ') if x][1])
    #             break
    
    #     return F_resonance
    
##############################################################################   
            
    def def_beta(self, F_target, CAV):     
        l = (CAV[0,6] + CAV[2,6])/1000
        lambda_2 = 299792458/(F_target*10**6)
        self.beta = round(2*l/(lambda_2),2)
        if self.beta > 1:
            self.beta = 1

##############################################################################   
            
    def p2g_f(self, CAV_py, n):
        #try:
        R_ir = CAV_py[0]
        alpha = CAV_py[1]*np.pi/180
        R = CAV_py[2]
        r = CAV_py[3]
        d = CAV_py[4]
        L = CAV_py[5]
        H = CAV_py[6]

        geom = Geometry()
        A,B,a,b,R_eq = geom.p2g_geom(R_ir,alpha,R,r,d,L,H)    
        # m = np.tan(3*np.pi/2+alpha)
        # a1 = m**2
        # b1 = m*((r**2+m**2)*(d-L)-m**2*(d-L)+L*r**2)
        # c1 = (m**2*(d-L)-L*r**2)**2-(r**2+m**2)*(L**2*r**2+m**2*(d-L)**2)
        
        # b = (-b1+np.sqrt(b1**2-a1*c1))/a1
        # a = b/r
                
        # Y0 = R_ir + b + H
        # a4 = R**2+m**2
        # b4 = m*(m*(d-L)+R_ir-Y0)
        # B = np.sqrt((m*(d-L)+R_ir-Y0)**2 - b4**2/a4)
        # A = B/R
        # R_eq = Y0 + B
        
        return [A, B, a, b, R_eq, R_ir, L]

##############################################################################
    
    def g2p_f(self, CAV_ge, n): 
        CAV = np.zeros((7))

        CAV[0] = CAV_ge[0]
        CAV[1] = CAV_ge[1]
        CAV[2] = CAV_ge[2]
        CAV[3] = CAV_ge[3]
        CAV[4] = CAV_ge[4]
        CAV[5] = CAV_ge[5]
        CAV[6] = CAV_ge[6]
        
        geom = Geometry()
        R_ir,alpha,R,r,d,L,H = geom.g2p_geom(CAV)
        # XYP = geom.racc_point(CAV)
        # #XYP = self.racc_point(CAV)
        # A = CAV[0]
        # B = CAV[1]
        # a = CAV[2]
        # b = CAV[3]
        # R_eq = CAV[4]
        # R_ir = CAV[5]       
        # L = CAV[6]
        # r = b/a
        # R = B/A
        # H = (R_eq-B)-(R_ir+b)
        # alpha = (np.arctan2(XYP[1,0]-XYP[0,0],XYP[0,1]-XYP[1,1]))*180/np.pi
        # m = (XYP[0,1]-XYP[1,1])/(XYP[0,0]-XYP[1,0])
        # d = L - (R_ir-XYP[1,1])/m - XYP[1,0] 
  
        return [R_ir, alpha, R, r, d, L, H]   
 