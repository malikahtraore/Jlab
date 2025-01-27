#### Electromagnetic simulations: management and creation of SUPERFISH files: AF, SGF
# For half cell, end group and multicell


from os import remove, listdir
from os.path import isdir, join, getsize, exists
import numpy as np
from subprocess import call as scall
from scipy.interpolate import CubicSpline
from shutil import rmtree, copyfile
from PyQt5.QtWidgets import QMessageBox

from Draw_cavity_profile import Draw_cavity_profile
from geometry import Geometry
from electromagnetic_functions import emfn

class Press_Button_ELMG_simulation():
    #def __init__(self, elmg_param, path, MATP, CAV, parent):
    def __init__(self, CAV, path,parent=None):
        #super(Press_Button_ELMG_simulation, self).__init__(parent)
        self.path = path
        #self.elmg_param = elmg_param
        self.Eacc = 10
        self.dx = CAV[0,4]/50
        #self.temp_type = self.elmg_param[2]
        self.temp_type = 2 # T = 2K
        #self.beta_type = self.elmg_param[3]
        self.beta_type = 1 # beta geom
        #self.part_acc = self.elmg_param[4]
        self.part_acc = 1 # = 1 proton, else = 2
        
        self.MATP = np.array([8.57E-6, 1.06E+5, 1.18E+5, 0.4, 0.38, 50, 1.52e-05, 0, 0.00146])

        #self.MATP = MATP
        self.CAV = CAV
        
        self.elmg_param=np.zeros(25)
        self.elmg_param[22]=-2
        self.parent=parent # used to recall some values from parent class BuildCav2
        self.new_parameter = getattr(self.parent, 'new_parameter', None)

        self.new_parameter_IC = getattr(self.parent, 'new_parameter_IC', None)
        self.new_parameter_EC = getattr(self.parent, 'new_parameter_EC', None)

##############################################################################
        
    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass 
               
##############################################################################
        
    def run_elmg_simulation(self): 
        
        try:
            self.make_SF_input_file()

            self.cold_cavity('AF_file', self.dx) # simulazioni a T = 2K   

            # Determina la frequenza di prmimo tentativo cioe self.F_guess
            self.f_guess(self.elmg_param[22])
            
            with open(self.path + '\\elmg_file\\AF_file.AF', 'r') as af_old:
                cont_af = af_old.readlines()

            af_old =  open(self.path+'\\elmg_file\\AF_file.AF', 'r')
            cont_af = af_old.readlines()
            af_old.close()  
            af_new =  open(self.path+'\\elmg_file\\AF_file.AF', 'w')
            
    
            #cont_af[6] = 'dx=' + str(self.dx) + ', freq=' +str(self.F_guess)+', ModT36 = 1 ,\n'   
            cont_af[6] = 'dx=' + str(self.dx) + ', freq=' +str(self.F_guess)+',\n'   
    
            cont_af_del = [x for x in cont_af[16].split(',') if x]
            cont_af[16] = cont_af_del[0]+ ',' + cont_af_del[1] + ', norm = 1, EZEROT = ' + str(self.Eacc*10**6) + '$ \n'
            
        
            cont_af_del = [x for x in cont_af[12].split(',') if x]
            cont_af[12] = cont_af_del[0] + ', rmass = -2,' + cont_af_del[2] + cont_af_del[3][0:-1] + ',\n'   
    
                                
            af_new.writelines(cont_af)
            af_new.close()
    
            #w=self.elmg_funtions(self.CAV, self.path)
            #w.run_elmg_simulation_part()
            
            self.def_beta_geom()
    
            scall(self.path+'\\elmg_file\\AF_file.AF', shell=True)

            self.write_SGF()
            scall(self.path+'\\elmg_file\\AF_file.SGF', shell=True)

            self.field_data()
        except:
            #self.warning_wdj('Errors during elmg simulation')
            print('warning')
    

##############################################################################   
        
    def make_SF_input_file(self):   
        if self.CAV[0,7] in list(range(1,16)):     
            x = Draw_cavity_profile(self.path, self.CAV, 1.4)
            geom=Geometry()
            CAV_PROF = x.CAV_Prof()
            if self.CAV[3,7]!=0 and self.CAV[2,7]==0:
                CAV_PROF += ['TU']
            ECs = self.CAV[0,:] #EC
            PCs = self.CAV[1,:] #PC
            IC = self.CAV[2,:] #IC
            ECd = self.CAV[3,:]
            PCd = self.CAV[4,:]  # 's' stands for left 'd' stands for right          
            
            Pecs = np.zeros((2,2))        
            Ppcs = np.zeros((2,2))  
            Pic = np.zeros((2,2)) 
            Pecd = np.zeros((2,2)) #starting and ending points of a straight line        
            Ppcd = np.zeros((2,2))  

            if np.all(self.CAV[0,0:-1] > 0):
                Pecs = geom.racc_point(ECs)
                #Pecs = x.racc_point(ECs)
            if np.all(self.CAV[1,0:-1] > 0):
                Ppcs = geom.racc_point(PCs)
                #Ppcs = x.racc_point(PCs)
            if np.all(self.CAV[2,0:-1] > 0):
                Pic = geom.racc_point(IC)
                #Pic = x.racc_point(IC)
            if np.all(self.CAV[0,0:-1] > 0):
                Pecd = geom.racc_point(ECd)
                #Pecd = x.racc_point(ECd)
            if np.all(self.CAV[1,0:-1] > 0):
                Ppcd = geom.racc_point(PCd)                
                #Ppcd = x.racc_point(PCd)                

            self.write_af_file(CAV_PROF, self.CAV, IC, Pic, PCs, Ppcs, ECs, Pecs, PCd, Ppcd, ECd, Pecd, self.path)
        else:
            self.write_af_OM_file()

##############################################################################  
        
    def write_af_file(self, CAV_PROF, CAV, IC, Pic, PCs, Ppcs, ECs, Pecs, PCd, Ppcd, ECd, Pecd, path):  
      ok = 1
      for filename in listdir(path+'\\elmg_file'):
          file_path = join(path+'\\elmg_file', filename)
          try:
              if isdir(file_path):
                  rmtree(file_path)
          except Exception as e:
              self.warning_wdj(f'File not deleted: {file_path}, {e}')
              return
              self.warning_not_deleted_file(file_path, e)
              ok = 0
              break
     
      if ok == 1: 
          l_cil_s1 = CAV[1,7]
          l_cil_d1 = CAV[2,7]
          l_cil_s2 = CAV[3,7]
          l_cil_d2 = CAV[4,7]
          dx = self.dx
          SM = np.zeros((len(CAV_PROF)+1))
          af_file =  open(path+'\\elmg_file\\AF_file.AM', 'w')
          lines = ['Simulation file:',
          ' ',   
          '$reg kprob=1, conv = 0.1,',
          'dx=' + str(dx) + ', freq=500,',
          'xdri=0.0, ydri=1',
          'nbslf=1, nbsrt=1, dslope =-1,',
          'beta=0.61, rmass = -2, kmethod=1, ',
          'irtype=1, tempk=2.0, tc=9.2, residr=0.0,',
          'clength=100.0, zctr=40, norm=1$',
          ' ',
          '$po x=0.0, y=0.0$']
          
          X_c = [] 
          X_c_sup = []
          sm_cont = 0
          for k in range(0,len(CAV_PROF)):
              if CAV_PROF[k] == 'TU':
                   if k == 0: # tubo sinistra
                       if l_cil_d1==0: # se tubo con L@iris=0
                           lines += ['$po x=0.0, y='+str(ECs[5])+'$']
                           X_c += [l_cil_s1]
                           lines += ['$po x='+str(l_cil_s1)+', y='+str(ECs[5])+'$']
                       else: # rubo con Liris non 0
                           lines += ['$po x=0.0, y='+str(IC[5])+'$']
                           lines += ['$po x='+str(l_cil_s1-l_cil_d1+IC[5]-ECs[5])+', y='+str(IC[5])+'$']
                           lines += ['$po x='+str(l_cil_s1-l_cil_d1)+', y='+str(ECs[5])+'$']
                           X_c += [l_cil_s1]
                           lines += ['$po x='+str(l_cil_s1)+', y='+str(ECs[5])+'$']
                   else: # tubo destro
                        #l_cil_d=0
                        if l_cil_d2 == 0: # tubo con L@iris =0
                            lines = lines + ['$po x='+str(X_c[-1]+l_cil_s2)+', y='+str(ECd[5])+'$']
                            X_c += [X_c[-1]+l_cil_s2]
                        else: # tubo con L@iris non 0
                            #X_c += [X_c[-1]+l_cil_d]
                            lines += ['$po x='+str(X_c[-1]+l_cil_d2)+', y='+str(ECd[5])+ '$']
                            #X_c += [X_c[-1] + np.abs(self.CAV[0,5]-self.CAV[2,5])]          
                            #lines += ['$po x='+str(X_c[-1])+', y='+str(IC[5])+ '$']            
                            #X_c += [IC[6] + PC[6] + l_cil_s]
                            lines += ['$po x='+str(X_c[-1]+l_cil_d2-IC[5]+ECd[5])+',y='+str(IC[5])+'$',
                                '$po x='+str(X_c[-1]+l_cil_s2)+', y='+str(IC[5])+ '$'] 
                            X_c += [X_c[-1]+l_cil_s2]
                       ## senza l_cil_d     
                      # if k == 0:
                      #     lines += ['$po x=0.0, y='+str(EC[5])+'$']
                      #     X_c += [l_cil_s]
                      #     lines += ['$po x='+str(l_cil_s)+', y='+str(EC[5])+'$']
                      # else:
                      #     lines = lines + ['$po x='+str(X_c[-1]+l_cil_d)+', y='+str(EC[5])+'$']
                      #     X_c += [X_c[-1]+l_cil_d]        
#writing the geometry for the left end half cell                 
              elif CAV_PROF[k] == 'ECs':
                  if k == 0:
                      lines += ['$po x=0.0, y='+str(ECs[5])+'$']
                      X_c += [0.0]
                  lines = lines + [
                  '$po NT=2, x0='+str(X_c[-1])+', y0='+str(ECs[5]+ECs[3])+', x='+str(ECs[6]-Pecs[1,0])+', y='+str(Pecs[1,1]-(ECs[5]+ECs[3]))+', A='+str(ECs[2])+', B='+str(ECs[3])+'$',
                  '$po x='+str(X_c[-1]+ECs[6]-Pecs[0,0])+ ', y ='+str(Pecs[0,1])+ '$',
                  '$po NT=2, x0='+str(X_c[-1]+ECs[6])+', y0='+str(ECs[4]-ECs[1])+', x= 0.0, y='+str(ECs[1])+', A='+str(ECs[0])+', B='+str(ECs[1])+'$']
                  if SM[sm_cont] != 0:
                      lines += ['$po x='+str(X_c[-1]+ECs[6]+SM[sm_cont])+', y='+str(ECs[4])+'$']
                  X_c_sup += [X_c[-1]+ECs[6]+SM[sm_cont]]
                  X_c += [X_c[-1]+ECs[6]+SM[sm_cont]]
                  sm_cont += 1
                           
              elif CAV_PROF[k] == 'ECd': #Writing the geometry for the right end half cell
                  if k == 0:
                      lines += ['$po x=0.0, y='+str(ECd[4])+'$']
                      if SM[sm_cont] != 0:
                          lines += ['$po x='+str(SM[sm_cont])+', y='+str(ECd[4])+'$']
                      X_c_sup += [SM[sm_cont]]
                      sm_cont += 1
                      X_c += [SM[sm_cont]]
                  lines = lines + [
                  '$po NT=2, x0='+str(X_c[-1])+', y0='+str(ECd[4]-ECd[1])+', x='+str(Pecd[0,0])+', y='+str(Pecd[0,1]-(ECd[4]-ECd[1]))+', A='+str(ECd[0])+', B='+str(ECd[1])+'$',
                  '$po x='+str(X_c[-1]+Pecd[1,0])+ ', y ='+str(Pecd[1,1])+ '$',
                  '$po NT=2, x0='+str(X_c[-1]+ECd[6])+', y0='+str(ECd[5]+ECd[3])+', x=0.0, y='+str(-ECd[3])+', A='+str(ECd[2])+', B='+str(ECd[3])+'$',] 
                  X_c += [X_c[-1]+ECd[6]]
                    
              elif CAV_PROF[k] == 'PCs':
                  if k == 0:
                      lines += ['$po x=0.0, y='+str(PCs[5])+'$']
                      X_c += [0.0]
                  lines += [
                  '$po NT=2, x0='+str(X_c[-1])+', y0='+str(PCs[5]+PCs[3])+', x='+str(PCs[6]-Ppcs[1,0])+', y='+str(Ppcs[1,1]-(PCs[5]+PCs[3]))+', A='+str(PCs[2])+', B='+str(PCs[3])+'$',
                  '$po x='+str(X_c[-1]+PCs[6]-Ppcs[0,0])+ ', y ='+str(Ppcs[0,1])+ '$',
                  '$po NT=2, x0='+str(X_c[-1]+PCs[6])+', y0='+str(PCs[4]-PCs[1])+', x= 0.0, y='+str(PCs[1])+', A='+str(PCs[0])+', B='+str(PCs[1])+'$']
                  if SM[sm_cont] != 0:
                      lines += ['$po x='+str(X_c[-1]+PCs[6]+SM[sm_cont])+', y='+str(PCs[4])+'$']
                  X_c_sup += [X_c[-1]+PCs[6]+SM[sm_cont]]
                  X_c += [X_c[-1]+PCs[6]+SM[sm_cont]]
                  sm_cont += 1
                          
              elif CAV_PROF[k] == 'PCd':
                  if k == 0:
                      lines += ['$po x=0.0, y='+str(PCd[4])+'$']
                      if SM[sm_cont] != 0:
                          lines += ['$po x='+str(SM[sm_cont])+', y='+str(PCd[4])+'$']
                      X_c_sup += [SM[sm_cont]]
                      sm_cont += 1
                      X_c += [SM[sm_cont]]
                  lines = lines + [
                  '$po NT=2, x0='+str(X_c[-1])+', y0='+str(PCd[4]-PCd[1])+', x='+str(Ppcd[0,0])+', y='+str(Ppcd[0,1]-(PCd[4]-PCd[1]))+', A='+str(PCd[0])+', B='+str(PCd[1])+'$',
                  '$po x='+str(X_c[-1]+Ppcd[1,0])+ ', y ='+str(Ppcd[1,1])+ '$',
                  '$po NT=2, x0='+str(X_c[-1]+PCd[6])+', y0='+str(PCd[5]+PCd[3])+', x=0.0, y='+str(-PCd[3])+', A='+str(PCd[2])+', B='+str(PCd[3])+'$']     
                  X_c += [X_c[-1]+PCd[6]]
          
              elif CAV_PROF[k] == 'ICs':
                  if k == 0:
                      lines += ['$po x=0.0, y='+str(IC[5])+'$']
                      X_c += [0.0]
                  lines += [
                  '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[5]+IC[3])+', x='+str(IC[6]-Pic[1,0])+', y='+str(Pic[1,1]-(IC[5]+IC[3]))+', A='+str(IC[2])+', B='+str(IC[3])+'$',
                  '$po x='+str(X_c[-1]+IC[6]-Pic[0,0])+ ', y ='+str(Pic[0,1])+ '$',
                  '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[4]-IC[1])+', x= 0.0, y='+str(IC[1])+', A='+str(IC[0])+', B='+str(IC[1])+'$']
                  if SM[sm_cont] != 0:
                      lines += ['$po x='+str(X_c[-1]+IC[6]+SM[sm_cont])+', y='+str(IC[4])+'$']  
                  X_c_sup += [X_c[-1]+IC[6]+SM[sm_cont]]
                  X_c += [X_c[-1]+IC[6]+SM[sm_cont]]
                  sm_cont += 1  
                  
              elif CAV_PROF[k] == 'ICd':
                  if k == 0:
                      lines += ['$po x=0.0, y='+str(IC[4])+'$']
                      if SM[sm_cont] != 0:          
                          lines += ['$po x='+str(SM[sm_cont])+', y='+str(IC[4])+'$']
                      X_c_sup += [SM[sm_cont]]
                      sm_cont += 1
                      X_c += [SM[sm_cont]]
                  lines = lines + [
                  '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[4]-IC[1])+', x='+str(Pic[0,0])+', y='+str(Pic[0,1]-(IC[4]-IC[1]))+', A='+str(IC[0])+', B='+str(IC[1])+'$',
                  '$po x='+str(X_c[-1]+Pic[1,0])+ ', y ='+str(Pic[1,1])+ '$',
                  '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[5]+IC[3])+', x=0.0, y='+str(-IC[3])+', A='+str(IC[2])+', B='+str(IC[3])+'$']
                  X_c += [X_c[-1]+IC[6]]
                          
          lines += ['$po x='+str(X_c[-1])+', y=0.0$',
                     '$po x=0.0, y=0.0$']  
          
          
          af_file.write('\n'.join(lines))
          af_file.close()
         
          ########################################
          
          scall(path+'\\elmg_file\\AF_file.AM', shell=True)
          corr_1_file  = open(path+'\\elmg_file\\AF_file.AM', 'r')
          cont = corr_1_file.readlines()
          corr_1_file.close()
          remove(path+'\\elmg_file\\AF_file.AM')
      
          ########################################
       
          self.ext_coo()
          if getsize(path+'\\elmg_file\\log_coo_base.txt') != 0:                               
              SC = np.loadtxt(path+'\\elmg_file\\log_coo_base.txt') 
              
              if len(X_c_sup) % 2 == 0:
                  dr_px = X_c_sup[int(len(X_c_sup)/2)-1]
              else:
                  dr_px = X_c_sup[int((len(X_c_sup)-1)/2-1)]
                  dr_px = X_c_sup[int((len(X_c_sup)-1)/2)]
              
              if dr_px == 0.0:
                  for k in range(1,len(SC)):
                      if SC[k,2] != 0 and SC[k-1,2] == 0:
                          dr_py = SC[k-1,3]
                          break
              else:
                  dr_py = SC[list(SC[:,2]).index(round(dr_px,4)),3]
                  dr_px = dr_px-SM[X_c_sup.index(dr_px)]/2
                         
              ######################################## 
              
              for k in range(0,len(cont)):
                  try:
                      if [x for x in cont[k].split(' ') if x][1] == 'NT=2,': 
                          if float([x for x in cont[k-1].split(' ') if x][2].split('=')[1][0:-2]) > ECs[5]: # ECs? o EC
                              clength_s = float([x for x in cont[k-1].split(' ') if x][1].split('=')[1][0:-1])
                          else:                
                              clength_s = float([x for x in cont[k].split(' ') if x][2].split('=')[1][0:-1])
                          break
                  except:
                      pass
                  
              for k in range(len(cont),0,-1):
                  try:
                      if [x for x in cont[k].split(' ') if x][1] == 'NT=2,':
                          if float([x for x in cont[k+1].split(' ') if x][2].split('=')[1][0:-2]) > ECs[5]: # ECs? o EC
                              clength_d = float([x for x in cont[k+1].split(' ') if x][1].split('=')[1][0:-1])
                          else: 
                              clength_d = float([x for x in cont[k].split(' ') if x][2].split('=')[1][0:-1])
                          break
                  except:
                      pass
                  
              ######################################## 
              
              corr_2_file  = open(path+'\\elmg_file\\AF_file.AF', 'w')
              cont[4] = 'xdri='+str(dr_px)+', ydri='+str(dr_py-dx*2)+',\n'
              cont[8] = 'clength='+str(clength_d-clength_s)+', zctr='+str(dr_px)+', norm=1$ \n'
              corr_2_file.write('\n'.join(cont))
              corr_2_file.close()
              
 
###############################################################################
        
    def write_af_OM_file(self):         
        x = Draw_cavity_profile(self.path, self.CAV, 1.4)
        geom=Geometry()
        EC = self.CAV[0,:]
        PC = self.CAV[1,:]
        IC = self.CAV[2,:]
        Pec = np.zeros((2,2))        
        Ppc = np.zeros((2,2))  
        Pic = np.zeros((2,2)) 
            
        if np.all(self.CAV[0,0:-1] > 0):
            Pec = geom.racc_point(EC)
            #Pec = x.racc_point(EC)
        if np.all(self.CAV[1,0:-1] > 0):
            Ppc = geom.racc_point(PC)
            #Ppc = x.racc_point(PC)
        if np.all(self.CAV[2,0:-1] > 0):
            Pic = geom.racc_point(IC)   
            #Pic = x.racc_point(IC)   
            
        if self.CAV[0,7] == 19: 
            l_cil = self.CAV[1,7]
        else:
            l_cil = 0
        
        dx = self.elmg_param[1]
        SM = [self.elmg_param[23], self.elmg_param[24]]
           
        af_file =  open(self.path + '\\elmg_file\\AF_file.AM', 'w')
        lines = ['Simulation file:',
        ' ',   
        '$reg kprob=1, conv = 0.1,',
        'dx=' + str(dx) + ', freq=500,',
        'xdri=0.0, ydri=1',
        'nbslf=1, nbsrt=1, dslope =-1,',
        'beta=0.61, rmass = -2, kmethod=1, ',
        'irtype=1, tempk=2.0, tc=9.2, residr=0.0,',
        'clength=100.0, zctr=40, norm=1$',
        ' ',
        '$po x=0.0, y=0.0$']
        
        dr_px = dx
        X_c = [] 
        if self.CAV[0,7] == 19:
            lines += ['$po x=0.0, y='+str(EC[5])+'$',  
            '$po x='+str(l_cil)+', y='+str(EC[5])+'$']
            X_c += [l_cil]
            lines += [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(EC[5]+EC[3])+', x='+str(EC[6]-Pec[1,0])+', y='+str(Pec[1,1]-(EC[5]+EC[3]))+', A='+str(EC[2])+', B='+str(EC[3])+'$',
            '$po x='+str(X_c[-1]+EC[6]-Pec[0,0])+ ', y ='+str(Pec[0,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+EC[6])+', y0='+str(EC[4]-EC[1])+', x= 0.0, y='+str(EC[1])+', A='+str(EC[0])+', B='+str(EC[1])+'$']
            X_c += [X_c[-1]+EC[6]+SM[0]]
            if SM[0] != 0:
                lines += ['$po x='+str(X_c[-1])+', y='+str(EC[4])+'$']
                
            dr_px = X_c[-1] 
            dr_py = EC[4] - dx
            clength = X_c[-1] - l_cil
            
        elif self.CAV[0,7] == 20:
            X_c += [0]              
            lines += ['$po x=0.0, y='+str(PC[4])+'$']
            if SM[0] != 0:
                lines += ['$po x='+str(SM[0])+', y='+str(PC[4])+'$']
                X_c += [SM[0]]
            lines = lines + [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(PC[4]-PC[1])+', x='+str(Ppc[0,0])+', y='+str(Ppc[0,1]-(PC[4]-PC[1]))+', A='+str(PC[0])+', B='+str(PC[1])+'$',
            '$po x='+str(X_c[-1]+Ppc[1,0])+ ', y ='+str(Ppc[1,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+PC[6])+', y0='+str(PC[5]+PC[3])+', x=0.0, y='+str(-PC[3])+', A='+str(PC[2])+', B='+str(PC[3])+'$']     
            X_c += [PC[6]+SM[0]]
            lines += [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[5]+IC[3])+', x='+str(IC[6]-Pic[1,0])+', y='+str(Pic[1,1]-(IC[5]+IC[3]))+', A='+str(IC[2])+', B='+str(IC[3])+'$',
            '$po x='+str(X_c[-1]+IC[6]-Pic[0,0])+ ', y ='+str(Pic[0,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[4]-IC[1])+', x= 0.0, y='+str(IC[1])+', A='+str(IC[0])+', B='+str(IC[1])+'$']
            X_c += [X_c[-1]+IC[6]+SM[1]]
            if SM[1] != 0:
                lines += ['$po x='+str(X_c[-1])+', y='+str(IC[4])+'$']  
       
            dr_py = PC[4] - dx
            clength = X_c[-1] 
        
        elif self.CAV[0,7] == 21:       
            X_c += [0]
            lines += ['$po x=0.0, y='+str(IC[4])+'$']
            if SM[0] != 0:          
                lines += ['$po x='+str(SM[0])+', y='+str(IC[4])+'$']
                X_c += [SM[0]]
            lines = lines + [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[4]-IC[1])+', x='+str(Pic[0,0])+', y='+str(Pic[0,1]-(IC[4]-IC[1]))+', A='+str(IC[0])+', B='+str(IC[1])+'$',
            '$po x='+str(X_c[-1]+Pic[1,0])+ ', y ='+str(Pic[1,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[5]+IC[3])+', x=0.0, y='+str(-IC[3])+', A='+str(IC[2])+', B='+str(IC[3])+'$']
            X_c += [IC[6]+SM[0]]
            lines += [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[5]+IC[3])+', x='+str(IC[6]-Pic[1,0])+', y='+str(Pic[1,1]-(IC[5]+IC[3]))+', A='+str(IC[2])+', B='+str(IC[3])+'$',
            '$po x='+str(X_c[-1]+IC[6]-Pic[0,0])+ ', y ='+str(Pic[0,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[4]-IC[1])+', x= 0.0, y='+str(IC[1])+', A='+str(IC[0])+', B='+str(IC[1])+'$']
            X_c += [X_c[-1]+IC[6]+SM[1]]
            if SM[1] != 0:
                lines += ['$po x='+str(X_c[-1])+', y='+str(IC[4])+'$']  
                
            dr_py = IC[4] - dx
            clength = X_c[-1] 

        elif self.CAV[0,7] == 16: # end cell
            #SM[0] = self.new_parameter
            X_c += [0]
            lines += ['$po x=0.0, y='+str(EC[4])+'$']
            if SM[0] != 0:
                lines += ['$po x='+str(SM[0])+', y='+str(EC[4])+'$']
                X_c += [SM[0]]
            lines = lines + [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(EC[4]-EC[1])+', x='+str(Pec[0,0])+', y='+str(Pec[0,1]-(EC[4]-EC[1]))+', A='+str(EC[0])+', B='+str(EC[1])+'$',
            '$po x='+str(X_c[-1]+Pec[1,0])+ ', y ='+str(Pec[1,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+EC[6])+', y0='+str(EC[5]+EC[3])+', x=0.0, y='+str(-EC[3])+', A='+str(EC[2])+', B='+str(EC[3])+'$',] 
            X_c += [X_c[-1]+EC[6]+SM[1]]
            if SM[1] != 0:
                lines += ['$po x='+str(X_c[-1])+', y='+str(EC[5])+'$']  
            
            dr_py = EC[4] - dx
            clength = X_c[-1] 
                    
        elif self.CAV[0,7] == 17: # pen cell
            #SM[0] = self.new_parameter
            X_c += [0]
            lines += ['$po x=0.0, y='+str(PC[4])+'$']
            if SM[0] != 0:
                lines += ['$po x='+str(SM[0])+', y='+str(PC[4])+'$']
                X_c += [SM[0]]
            lines = lines + [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(PC[4]-PC[1])+', x='+str(Ppc[0,0])+', y='+str(Ppc[0,1]-(PC[4]-PC[1]))+', A='+str(PC[0])+', B='+str(PC[1])+'$',
            '$po x='+str(X_c[-1]+Ppc[1,0])+ ', y ='+str(Ppc[1,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+PC[6])+', y0='+str(PC[5]+PC[3])+', x=0.0, y='+str(-PC[3])+', A='+str(PC[2])+', B='+str(PC[3])+'$']     
            X_c += [X_c[-1]+PC[6]+SM[1]]
            if SM[1] != 0:
                lines += ['$po x='+str(X_c[-1])+', y='+str(PC[5])+'$']  
    
            dr_py = PC[4] - dx
            clength = X_c[-1] 
    
        elif self.CAV[0,7] == 18: # inner cell --> Start to be modified
            X_c += [0]
            #SM[0] = self.new_parameter
            lines += ['$po x=0.0, y='+str(IC[4])+'$']
            if SM[0] != 0:          
                lines += ['$po x='+str(SM[0])+', y='+str(IC[4])+'$']
                X_c += [SM[0]]
            lines = lines + [
            '$po NT=2, x0='+str(X_c[-1])+', y0='+str(IC[4]-IC[1])+', x='+str(Pic[0,0])+', y='+str(Pic[0,1]-(IC[4]-IC[1]))+', A='+str(IC[0])+', B='+str(IC[1])+'$',
            '$po x='+str(X_c[-1]+Pic[1,0])+ ', y ='+str(Pic[1,1])+ '$',
            '$po NT=2, x0='+str(X_c[-1]+IC[6])+', y0='+str(IC[5]+IC[3])+', x=0.0, y='+str(-IC[3])+', A='+str(IC[2])+', B='+str(IC[3])+'$']
            X_c += [X_c[-1]+IC[6]+SM[1]]
            if SM[1] != 0:
                lines += ['$po x='+str(X_c[-1])+', y='+str(IC[5])+'$'] 
                
            dr_py = IC[4] - dx
            clength = X_c[-1] 
                        
        lines += ['$po x='+str(X_c[-1])+', y=0.0$',
                  '$po x=0.0, y=0.0$']  
        
        af_file.write('\n'.join(lines))
        af_file.close()
        self.sbc_length = X_c[-1] 
        
        ########################################
        
        scall(self.path + '\\elmg_file\\AF_file.AM', shell=True)    
        corr_1_file  = open(self.path + '\\elmg_file\\AF_file.AM', 'r')
        cont = corr_1_file.readlines()
        corr_1_file.close()
        remove(self.path + '\\elmg_file\\AF_file.AM')
        
        ########################################

        self.ext_coo()
        corr_2_file  = open(self.path + '\\elmg_file\\AF_file.AF', 'w')
        cont[4] = 'xdri=' + str(dr_px) + ', ydri=' + str(dr_py) + ',\n'
        cont[8] = 'clength=' + str(clength) + ', zctr=' + str(dr_px) + ', norm=1$ \n'
        corr_2_file.write('\n'.join(cont))
        corr_2_file.close()
     
##############################################################################
        
    def ext_coo(self): 
        outaut_file  = open(self.path+'\\elmg_file\\OUTAUT.TXT', 'r')
        cont = outaut_file.readlines()
        table = []
        ok = 0
        for k in range(0,len(cont)):
            if [x for x in cont[k].split(' ') if x] == ['K', 'L', 'X', 'Y\n']:
                ok = 1
            elif ok == 1:
                try:
                    int([x for x in cont[k].split(' ') if x][0])
                    table = table + [cont[k]]
                except ValueError:
                    break
        outaut_file.close()    
          
        lcoo_file  = open(self.path+'\\elmg_file\\log_coo_base.txt', 'w')  
        lcoo_file.write(''.join(table))
        lcoo_file.close()                                             
                
##############################################################################         
        
    def RT_cavity(self):  
        af_old =  open(self.path+'\\elmg_file\\AF_file.AF', 'r')
        cont_af = af_old.readlines()
        af_old.close() 
        
        af_new =  open(self.path+'\\elmg_file\\AF_file.AF', 'w')        
        cont_af[14] = 'irtype=0, rhor='+str(self.MATP[6])+', tempr=20,\n'           
        af_new.writelines(cont_af)
        af_new.close()
        
        
    def cold_cavity(self, cavity_name, dx):  

        af_old =  open(self.path+'\\elmg_file\\'+cavity_name+'.AF', 'r')
        cont_af = af_old.readlines()
        af_old.close() 


        af_new =  open(self.path+'\\elmg_file\\'+cavity_name+'.AF', 'w') 
        cont_af[14] = 'irtype=1, tempk=2.0, tc=9.2, residr=0.0,\n'           
        af_new.writelines(cont_af)
        af_new.close()
        
        self.log_coordinates(cavity_name, dx)
        alfa = self.MATP[-1]
        alfa = 0
        LC = np.loadtxt(self.path + '\\elmg_file\\log_coo.txt')         
        
        table = [] 
        t36_file  = open(self.path + '\\elmg_file\\'+cavity_name+'.T36', 'w')  
        for k in range(0,len(LC)):
            table += [str(int(LC[k,0]))+','+str(int(LC[k,1]))+','+str(LC[k,2]*(1-alfa))+','+ str(LC[k,3]*(1-alfa))]

        t36_file.write('\n'.join(table))
        t36_file.close() 

        
##############################################################################       
        
    def log_coordinates(self, cavity_name, dx):     
        
        copyfile(self.path+'\\elmg_file\\'+cavity_name+'.AF',self.path+'\\elmg_file\\'+cavity_name+'.AM')
        #scall('copy '+self.path+'\\elmg_file\\'+cavity_name+'.AF '+self.path+'\\elmg_file\\'+cavity_name+'.AM', shell=True)        
        
        af_old =  open(self.path+'\\elmg_file\\'+cavity_name+'.AM', 'r')
        cont_af = af_old.readlines()
        af_old.close()  
        af_new =  open(self.path+'\\elmg_file\\'+cavity_name+'.AM', 'w')        
        cont_af[6] = 'dx=' + str(dx) + ', freq=500,\n'           
        af_new.writelines(cont_af)
        af_new.close()
        
        scall(self.path+'\\elmg_file\\' + cavity_name + '.AM', shell=True) 
        
        outaut_file  = open(self.path+'\\elmg_file\\OUTAUT.TXT', 'r')
        cont = outaut_file.readlines()
        table = []
        ok = 0
        for k in range(0,len(cont)):
            if [x for x in cont[k].split(' ') if x] == ['K', 'L', 'X', 'Y\n']:
                ok = 1
            elif ok == 1:
                try:
                    int([x for x in cont[k].split(' ') if x][0])
                    table = table + [cont[k]]
                except ValueError:
                    break
        outaut_file.close()    
          
        lcoo_file  = open(self.path+'\\elmg_file\\log_coo.txt', 'w')  
        lcoo_file.write(''.join(table))
        lcoo_file.close() 
        
############################################################################### 

    def f_guess(self, modo): 
        if self.CAV[0,7] in [1, 19] or modo == -1:
            self.F_guess = 500
        elif modo == -2:
            if self.CAV[0,7] in list(range(1,16)):
                if self.CAV[0,7] == 2:
                   EC = self.CAV[1,:]
                   #PC = self.CAV[1,:]
                else:
                   EC = self.CAV[2,:]
            else:
                if self.CAV[0,7] in [18, 21]:
                    EC = self.CAV[2,0:7]
                elif self.CAV[0,7] == 20:
                    EC = self.CAV[1, 0:7]
                elif self.CAV[0,7] == 16:
                    EC = self.CAV[0,0:7]
                elif self.CAV[0,7] == 17:
                    EC = self.CAV[1,0:7]
        
            x = Draw_cavity_profile(self.path, self.CAV, self.dx)
            geom=Geometry()
            Pec = geom.racc_point(EC) 
            #Pec = x.racc_point(EC) 
                 
            part_name = 'AF_file_FG'
            af_file =  open(self.path+'\\elmg_file\\' + part_name + '.AF', 'w')

            # if self.CAV[0,7] == 2:
            #     Ppc = x.racc_point(PC)
            #     lines = ['Simulation for frequency guess\n',
            #     ' \n',   
            #     '$reg kprob=1, conv = 0.1,\n',
            #     'dx='+str(self.dx*self.CAV[0,7])+' , freq=500,\n',
            #     'xdri=' + str(EC[6]) + ', ydri='+ str(EC[4]-self.dx*self.CAV[0,7]) +',\n',
            #     'nbslf=1, nbsrt=1, dslope =-1,\n',
            #     'beta=0.67, rmass = -2, kmethod=1, \n',
            #     'irtype=1, tempk=2.0, tc=9.2, residr=0.0,\n',
            #     'clength='+ str(EC[6] + PC[6]) +', zctr = 0, norm=1, EZEROT = 1 $\n',
            #     ' ',
            #     '$po x=0.0, y=0.0$',    
            #     '$po x=0.0, y='+str(EC[5])+'$',
            #     '$po NT=2, x0=0.0, y0='+str(EC[5]+EC[3])+', x='+str(EC[6]-Pec[1,0])+', y='+str(Pec[1,1]-(EC[5]+EC[3]))+', A='+str(EC[2])+', B='+str(EC[3])+'$',
            #     '$po x='+str(EC[6]-Pec[0,0])+ ', y ='+str(Pec[0,1])+ '$',
            #     '$po NT=2, x0='+str(EC[6])+', y0='+str(EC[4]-EC[1])+', x= 0.0, y='+str(EC[1])+', A='+str(EC[0])+', B='+str(EC[1])+'$',
                
            
            #     '$po NT=2, x0='+str(EC[6])+', y0='+str(PC[4]-PC[1])+', x='+str(Ppc[0,0])+', y='+str(Ppc[0,1]-(PC[4]-PC[1]))+', A='+str(PC[0])+', B='+str(PC[1])+'$',
            #     '$po x='+str(EC[6] + Ppc[1,0])+ ', y ='+str(Ppc[1,1])+ '$',
            #     '$po NT=2, x0='+str(EC[6] + PC[6])+', y0='+str(PC[5]+PC[3])+', x=0.0, y='+str(-PC[3])+', A='+str(PC[2])+', B='+str(PC[3])+'$',
            #     '$po x='+str(EC[6] + PC[6])+', y=0.0$',
            #     '$po x=0.0, y=0.0$']    
            #     dx = self.dx*self.CAV[0,7] 
                                   
            # else:
            lines = ['Simulation for frequency guess\n',
            ' \n',   
            '$reg kprob=1, conv = 0.1,\n',
            'dx='+str(self.dx)+' , freq=500,\n',
            'xdri=0.001, ydri='+ str(EC[4]) +',\n',
            'nbslf=1, nbsrt=0, dslope =-1,\n',
            'beta=0.67, rmass = -2, kmethod=1, \n',
            'irtype=1, tempk=2.0, tc=9.2, residr=0.0,\n',
            'clength='+ str(EC[6]) +', zctr = 0, norm=1, EZEROT = 1 $\n',
            ' ',
            '$po x=0.0, y=0.0$',
            '$po x=0.0, y='+str(EC[4])+'$',
            '$po NT=2, x0=0.0, y0='+str(EC[4]-EC[1])+', x='+str(Pec[0,0])+', y='+str(Pec[0,1]-(EC[4]-EC[1]))+', A='+str(EC[0])+', B='+str(EC[1])+'$',
            '$po x='+str(Pec[1,0])+ ', y ='+str(Pec[1,1])+ '$',
            '$po NT=2, x0='+str(EC[6])+', y0='+str(EC[5]+EC[3])+', x=0.0, y='+str(-EC[3])+', A='+str(EC[2])+', B='+str(EC[3])+'$',
            '$po x='+str(EC[6])+', y=0.0$',
            '$po x=0.0, y=0.0$'] 
            dx = self.dx
                
            af_file.write('\n'.join(lines))
            af_file.close()

            if self.temp_type == 1:
                af_old =  open(self.path+'\\elmg_file\\'+part_name+'.AF', 'r')
                cont_af = af_old.readlines()
                af_old.close() 
                
                af_new =  open(self.path+'\\elmg_file\\'+part_name+'.AF', 'w')        
                cont_af[14] = 'irtype=0, rhor='+str(self.MATP[6])+', tempr=20,\n'           
                af_new.writelines(cont_af)
                af_new.close()  
            elif self.temp_type == 2:
                self.cold_cavity(part_name, dx)             
                af_old =  open(self.path+'\\elmg_file\\'+part_name+'.AF', 'r')
                cont_af = af_old.readlines()
                af_old.close()  
                af_new =  open(self.path+'\\elmg_file\\'+part_name+'.AF', 'w')        
                #cont_af[6] = 'dx=' + str(dx) + ', freq=500, ModT36 = 1 ,\n'           
                cont_af[6] = 'dx=' + str(dx) + ', freq=500,\n'           
                af_new.writelines(cont_af)
                af_new.close()             

            if self.CAV[0,7] in [16, 17, 18]:
                p1 = self.path+'\\elmg_file\\' + part_name + '.AF'
                p2 = self.path+'\\elmg_file\\AF_file.AF'
                copyfile(p1, p2)
            
            scall(self.path+'\\elmg_file\\' + part_name + '.AF', shell=True) 
            emfn1 = emfn()
            self.F_guess = emfn1.Resonance_frequency(self.path)
            #self.F_guess = self.Resonance_frequency()
        else:
            self.F_guess = float(modo)
            
###############################################################################    
    
    # def Resonance_frequency(self):
    #     sfo_file  = open(self.path+'\\elmg_file\\OUTFIS.TXT', 'r')
    #     cont = sfo_file.readlines()
    #     for k in range(len(cont)-1,0,-1):
    #         if str([x for x in cont[k].split(' ') if x][0]) == 'FREQ':
    #             F_resonance = float([x for x in cont[k].split(' ') if x][1])
    #             break
    #     sfo_file.close()
            
    #     return F_resonance       
        
############################################################################### 

    def def_beta_optim(self):
        file  = open(self.path+'\\elmg_file\\AF_file.AF', 'r')
        testo = file.readlines()
        file.close()        
        
        save_l_ch = testo[12]
        l_ch = [x for x in testo[12].split(',') if x]
        l_ch = l_ch[0:-1] + ['IBETA = 1, BETA1 = 0.5, BETA2 = 0.8, DBETA = 0.01\n']
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
        
        b_p_int = np.linspace(0.5,0.8, 1000)
        indx = np.where(f(b_p_int) == f(b_p_int).max())[0][0]
        
        toll = 1e-8
        err = 1
        x1 = b_p_int[indx-1]
        x2 = b_p_int[indx+1]
        while err > toll:
            x3 = (x1 + x2) * 0.5
            if df(x3) > 0 and df(x1) < 0:
                x2 = x3
            elif df(x3) > 0 and df(x2) < 0:
                x1 = x3
            elif df(x3) < 0 and df(x1) > 0:
                x2 = x3
            if df(x3) < 0 and df(x2) > 0:
                x1 = x3
            err = df(x3)
            
        self.beta = x3
        
        af_old =  open(self.path+'\\elmg_file\\AF_file.AF', 'r')
        cont_af = af_old.readlines()
        af_old.close()
        af_new =  open(self.path+'\\elmg_file\\AF_file.AF', 'w')                
        cont_af_del = [x for x in cont_af[12].split(',') if x] 
        cont_af[12] = 'beta=' + str(self.beta) + ',' + cont_af_del[1] + ',' + cont_af_del[2] + ',\n'
        af_new.writelines(cont_af)
        af_new.close()

############################################################################### 

    def def_beta_geom(self):
        if self.CAV[0,7] in list(range(1,16)):
            af_old =  open(self.path+'\\elmg_file\\AF_file.AF', 'r')
            cont_af = af_old.readlines()
            af_old.close()
            l = float([x for x in [x for x in cont_af[16].split(',') if x][0].split('=') if x][1])/1000
            lambda_2 = 299792458/(2*self.F_guess*10**6)
            N = self.CAV[0,7]
            self.beta = round(l/(N*lambda_2),2)
            if self.beta > 1:
                self.beta = 1
                    
            af_new =  open(self.path+'\\elmg_file\\AF_file.AF', 'w')                
            cont_af_del = [x for x in cont_af[12].split(',') if x] 
            cont_af[12] = 'beta=' + str(self.beta) + ',' + cont_af_del[1] + ',' + cont_af_del[2] + ',\n'
            af_new.writelines(cont_af)
            af_new.close() 
        else:
            af_old =  open(self.path+'\\elmg_file\\AF_file.AF', 'r')
            cont_af = af_old.readlines()
            af_old.close()
            l = float([x for x in [x for x in cont_af[16].split(',') if x][0].split('=') if x][1])/1000
            lambda_2 = 299792458/(2*self.F_guess*10**6)
            if self.CAV[0,7] in [16, 17, 18, 19]:
                N = 1
            elif self.CAV[0,7] in [20, 21]:
                N = 2
            self.beta = round(l/(N*lambda_2),2)
            if self.beta > 1:
                self.beta = 1
                    
            af_new =  open(self.path+'\\elmg_file\\AF_file.AF', 'w')                
            cont_af_del = [x for x in cont_af[12].split(',') if x] 
            cont_af[12] = 'beta=' + str(self.beta) + ',' + cont_af_del[1] + ',' + cont_af_del[2] + ',\n'
            af_new.writelines(cont_af)
            af_new.close()

###############################################################################
        
    def write_SGF(self):      
        sfo_file  = open(self.path+'\\elmg_file\\AF_file.SFO', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        
        for k in range(len(cont)):
            if cont[k] == 'Segment numbers for field calculations\n':
                indx = k+2
                break
        
        segments = []
        for k in range(indx,len(cont)):
            try:
               segments += [int([x for x in cont[k].split(' ') if x][-1][0:-1])]
            except:
                break
            
        sgf_file =  open(self.path+'\\elmg_file\\AF_file.SGF', 'w')
        lines = ['; SEGFIELD control file',
        'OUTPUT_file AF_file',
        'INPUT_filename AF_file.SFO',
        ' ',
        'SEGment_numbers      2 to ' + str(segments[-1]),
        ';E0T' + str(self.Eacc),
        'NodesOnly',
        'ENDFILE']
        sgf_file.write('\n'.join(lines))
        sgf_file.close()

###############################################################################        

    def field_data(self):
        # Generate cavity coordinate file
        tbl_file  = open(self.path+'\\elmg_file\\AF_file.TBL', 'r')
        cont = tbl_file.readlines()
        unit_press = 'Pa'
        for k in range(0,len(cont)):
            if [x for x in cont[k].split(' ') if x][0:-1] == [';', 'Z', 'R', 'S', 'E', 'H', 'P.D.', 'P']:
                n_begin = k+1
                if [x for x in cont[k].split(' ') if x][-1] == '(kPa)\n':
                    unit_press = 'kPa'
            elif cont[k][0:7] == 'EndData':
                n_end = k
        tbl_file.close()
        
        fd_file  = open(self.path + '\\elmg_file\\field_data.txt', 'w')
        fd_file.writelines(cont[n_begin : n_end])
        fd_file.close()
        
        if unit_press == 'kPa':
            DAT = np.loadtxt(self.path + '\\elmg_file\\field_data.txt')
            DAT[:,6] *= 10**3
            np.savetxt(self.path + '\\elmg_file\\field_data.txt', DAT)  

##############################################################################
            
    def output_result(self):
        sfo_file  = open(self.path+'\\elmg_file\\AF_file.SFO', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        
        emfn = emfn()
        self.elmg_param[5] = str(emfn.Resonance_frequency())
        #self.elmg_param[5] = str(self.Resonance_frequency())

        for k in range(len(cont)-1,0,-1):
            line = [x for x in cont[k].strip().split(' ') if x]
            try:
                if line[0] == 'Frequency':
                    self.elmg_param[6] = line[-1]
                    break
                elif line[0] == 'Transit-time':
                    self.elmg_param[7] = line[-1]
                elif line[0] == 'Stored':
                    self.elmg_param[8] = line[-2] 
                    self.elmg_param[9] = line[-1]   
                elif line[0] == 'Power':
                    self.elmg_param[10] = line[-2] 
                    self.elmg_param[11] = line[-1]     
                elif line[0] == 'Surface' or line[1] == 'surface':
                    self.elmg_param[12] = line[-2] 
                    self.elmg_param[13] = line[-1]  
                elif line[0] == 'Q':
                    self.elmg_param[14] = line[2] 
                    self.elmg_param[15] = line[-2]  
                    self.elmg_param[16] = line[-1]
                elif line[0] == 'Rs*Q':
                    self.elmg_param[17] = line[2] 
                    self.elmg_param[18] = line[3]  
                elif line[0] == 'r/Q':
                    self.elmg_param[19] = line[2] 
                    self.elmg_param[20] = line[3]        
            except:
                pass
        self.elmg_param[21] = self.beta
        
        return self.elmg_param
    
    # SuperFish file for IC --> file modified for the new parameter
    def IC_SF(self, F_guess, dx, IC, beta, Pic):
        SM=self.new_parameter

        # lines = [
        # 'Simulation file:',
        # ' ',   
        # '$reg kprob=1, conv = 0.1,',
        # 'dx=' + str(dx) + ', freq=' + str(F_guess) + ',',
        # 'xdri=0.0, ydri=' + str(IC[4] - dx) + ',',
        # 'nbslf=1, nbsrt=0, dslope =-1,',
        # 'beta=' + str(beta) + ', rmass = -2, kmethod=1, ',
        # 'irtype=1, tempk=2.0, tc=9.2, residr=0.0,',
        # 'clength=' + str(IC[6]) + ', zctr=0.0, norm=1 , EZEROT = 10000000$ \n',
        # ' ',
        # '$po x=0.0, y=0.0$',
        # ' ',
        # '$po x=0.0, y='+str(IC[4])+'$',
        # '$po NT=2, x0='+str(0.0)+', y0='+str(IC[4]-IC[1])+', x='+str(Pic[0,0])+', y='+str(Pic[0,1]-(IC[4]-IC[1]))+', A='+str(IC[0])+', B='+str(IC[1])+'$',
        # '$po x='+str(Pic[1,0])+ ', y ='+str(Pic[1,1])+ '$',
        # '$po NT=2, x0='+str(IC[6])+', y0='+str(IC[5]+IC[3])+', x=0.0, y='+str(-IC[3])+', A='+str(IC[2])+', B='+str(IC[3])+'$',
        # '$po x='+str(IC[6])+', y=0.0$',
        # '$po x=0.0, y=0.0$']  
        lines = [
        'Simulation file:',
        ' ',   
        '$reg kprob=1, conv = 0.1,',
        'dx=' + str(dx) + ', freq=' + str(F_guess) + ',',
        'xdri=0.0, ydri=' + str(IC[4] - dx) + ',',
        'nbslf=1, nbsrt=0, dslope =-1,',
        'beta=' + str(beta) + ', rmass = -2, kmethod=1, ',
        'irtype=1, tempk=2.0, tc=9.2, residr=0.0,',
        'clength=' + str(IC[6]) + ', zctr=0.0, norm=1 , EZEROT = 10000000$ \n',
        ' ',
        '$po x=0.0, y=0.0$',
        '$po x=0.0, y='+str(IC[4])+'$']

        if SM != 0:
                lines += ['$po x='+str(SM)+', y='+str(IC[4])+'$']
        lines+=[
        ' ',
        '$po NT=2, x0='+str(0.0+SM)+', y0='+str(IC[4]-IC[1])+', x='+str(Pic[0,0])+', y='+str(Pic[0,1]-(IC[4]-IC[1]))+', A='+str(IC[0])+', B='+str(IC[1])+'$',
        '$po x='+str(Pic[1,0]+SM)+ ', y ='+str(Pic[1,1])+ '$',
        '$po NT=2, x0='+str(IC[6]+SM)+', y0='+str(IC[5]+IC[3])+', x=0.0, y='+str(-IC[3])+', A='+str(IC[2])+', B='+str(IC[3])+'$',
        '$po x='+str(IC[6]+SM)+', y=0.0$',
        '$po x=0.0, y=0.0$'] 
        return lines

    # SuperFish file EG
    def EG_SF(self, F_guess, dx, IC, beta, EC, Pic, Pec, l_tube_Rir, l_tube, CAV):
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

        # to consider the new parameters in the SuperFish simulation: new_parameter_IC and new_parameter_EC are
        # the equator_length for IC (PC) and EC rispectively
        if self.new_parameter_IC != 0: # add by Elisa
            lines += [
                '$po x='+str(X_c[-1]+IC[6]+self.new_parameter_IC)+', y='+str(IC[4]-IC[1]+IC[1])+'$'
            ]
        if self.new_parameter_EC != 0:
                        lines += [
                '$po x='+str(X_c[-1]+IC[6]+self.new_parameter_IC+self.new_parameter_EC)+', y='+str(IC[4]-IC[1]+IC[1])+'$'
            ]

        X_c += [IC[6]+self.new_parameter_IC+self.new_parameter_EC]

        lines += [
        '$po NT=2, x0='+str(X_c[-1])+', y0='+str(EC[4]-EC[1])+', x='+str(Pec[0,0])+', y='+str(Pec[0,1]-(EC[4]-EC[1]))+', A='+str(EC[0])+', B='+str(EC[1])+'$',
        '$po x='+str(X_c[-1]+Pec[1,0])+ ', y ='+str(Pec[1,1])+ '$',
        '$po NT=2, x0='+str(X_c[-1]+EC[6])+', y0='+str(EC[5]+EC[3])+', x=0.0, y='+str(-EC[3])+', A='+str(EC[2])+', B='+str(EC[3])+'$',]

        X_c += [X_c[-1]+EC[6]]
        
        if l_tube_Rir == 0 and l_tube!=0:
            X_c += [X_c[-1]+l_tube]
            lines += ['$po x='+str(X_c[-1])+', y='+str(EC[5])+ '$',
            '$po x='+str(X_c[-1])+', y=0.0$',
            '$po x=0.0, y=0.0$'] 
        elif l_tube_Rir !=0 and l_tube!=0:
            
            # modifica L tube @ Riris
            X_c += [X_c[-1]+l_tube_Rir]
            lines += ['$po x='+str(X_c[-1])+', y='+str(EC[5])+ '$']
            X_c += [X_c[-1]+CAV[0,5]-CAV[2,5]]
            lines += ['$po x='+str(X_c[-1])+', y='+str(IC[5])+ '$']
            X_c += [X_c[-3]+l_tube]
            lines += ['$po x='+str(X_c[-1])+', y='+str(IC[5])+ '$', 
            '$po x='+str(X_c[-1])+', y=0.0$',
            '$po x=0.0, y=0.0$'] 

        else:
            lines += ['$po x='+str(X_c[-1])+', y=0.0$',
            '$po x=0.0, y=0.0$'] 
        return lines