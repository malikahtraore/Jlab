'''
- Defines the coordinate used to plot the profile of HC, EG or multicell
- Check continuity between iris radius dimensions
- circ_arc and ellipse_arc are used for the geometry profile design
'''

import numpy as np
from scipy.optimize import root
from scipy.special import ellipeinc
from geometry import Geometry

class Draw_cavity_profile():
    def __init__(self, path, CAV, dx, new_parameter, parent=None): # modified by Elisa
        self.path = path
        self.CAV = CAV # 0,6 e' la L
        self.Ncell = int(CAV[0,-1])
        self.l_cil_s = CAV[1,-1]
        self.l_cil_d = CAV[2,-1]
        self.dx = dx
        
        #self.new_parameter=parent.new_parameter
        self.new_parameter=new_parameter # new parameter: equator length
        self.CAV[0,6]-=self.new_parameter # new: substitute the half cell length with the half cell length - 
        # equator length in order to mantain all the functions. At the end of the draw just move all the
        # coordinates by the new_parameter.
        #### --> sbagliato: il new parameter va usato per sistemare il semiasse x dell'ellisse all'equatore ovvero A
        ##self.CAV[0,0]+=self.new_parameter # not this line. This line should be used if the parameter to modify is the equator X semi axes


        #self.CAV[0,6]=self.CAV[0,6]-self.LEQ


###############################################################################  

    # it defines the cavity profile coordinates --> used to draw the profile in draw.py           
    def CAV_coo(self):
        CAV_PROF = self.CAV_Prof()
        self.XC_param = []
        CAV_prof = []
        x_end = 0
        
        for k in range(len(CAV_PROF)):   

            if CAV_PROF[k] == 'TU': # tube
                if k == 0:
                    l_cil = self.l_cil_s
                else:
                    l_cil = self.l_cil_d
                sc_prof = np.zeros((int(l_cil/self.dx),2))
                sc_prof[:,0] = np.linspace(0, l_cil, int(l_cil/self.dx))
                sc_prof[:,1] = np.ones((int(l_cil/self.dx))) * self.CAV[0,5]
                if k == 0:
                    x_end = sc_prof[-1,0]
                    CAV_prof += np.delete(sc_prof, -1, 0).tolist()
                else:
                    sc_prof = np.delete(sc_prof, 0, 0)
                    x_add = sc_prof[-1,0]
                    sc_prof[:,0] += x_end
                    x_end += x_add
                    CAV_prof += sc_prof.tolist()
            else:
                if CAV_PROF[k][0] == 'E':
                    cell_data = self.CAV[0,:]
                elif CAV_PROF[k][0] == 'P':
                    cell_data = self.CAV[1,:]
                elif CAV_PROF[k][0] == 'I':
                    cell_data = self.CAV[2,:] 
                
                sc_prof = self.half_cell_coo(cell_data,self.new_parameter) # here you have to add the new parameter

                if len(sc_prof) == 0:
                    return []
                    break
                
                if CAV_PROF[k][2] == 's':
                    sc_prof[:,0] = np.ones(len(sc_prof))*sc_prof[-1,0]-sc_prof[:,0]    
                    sc_prof = np.flip(sc_prof, axis = 0)
                    self.XC_param += [sc_prof[-1,0] + x_end]

                x_add = sc_prof[-1,0]
                sc_prof[:,0] += x_end
                x_end += x_add # 79
                sc_prof = np.delete(sc_prof, -1, 0) # togliere commento
                CAV_prof += sc_prof.tolist()

        CAV_prof = np.array(self.add_last_point(CAV_prof))
        #CAV_prof = np.delete(CAV_prof, -1, 0)

        if self.check_continuity(CAV_prof):
            return CAV_prof
        else:
            return []

###############################################################################  
    # check continuity between iris radius dimensions for EG and multicell
    def check_continuity(self, CAV_prof):
        check = True       
        if self.CAV[0,4] != self.CAV[1,4] and self.CAV[0, 7] in list(range(2,16)):
            check = False
        if self.CAV[1,5] != self.CAV[2,5] and self.CAV[0, 7] in list(range(3, 16)) + [20]:
            check = False
            
        return check
        
###############################################################################  
    # add the last point coordinate depending on what you are plotting (HC, EG, ...)        
    def add_last_point(self, CAV_prof):
        if self.CAV[0,7] == 1:
            Sum = self.l_cil_s + self.l_cil_d + self.CAV[0,6]*2 
            CAV_prof += [[Sum, self.CAV[0,5]]]
        elif self.CAV[0,7] == 2:
            Sum = self.l_cil_s + self.l_cil_d + self.CAV[0,6]*2 + self.CAV[1,6]*2
            CAV_prof += [[Sum, self.CAV[0,5]]]            
        elif self.CAV[0,7] in list(range(3,16)):
            Sum = self.l_cil_s + self.l_cil_d + self.CAV[0,6]*2 + self.CAV[1,6]*2 + self.CAV[2,6]*(self.CAV[0,7]-2)*2
            CAV_prof += [[Sum, self.CAV[0,5]]]
        elif self.CAV[0,7] == 16:
            #CAV_prof += [[self.CAV[0,6], self.CAV[0,5]]]
            CAV_prof += [[self.CAV[0,6]+self.new_parameter, self.CAV[0,5]]]
        elif self.CAV[0,7] == 17:
            CAV_prof += [[self.CAV[1,6], self.CAV[1,5]]]
        elif self.CAV[0,7] == 18:
            CAV_prof += [[self.CAV[2,6], self.CAV[2,5]]]
        elif self.CAV[0,7] == 19:
            CAV_prof += [[self.l_cil_s + self.CAV[0,6], self.CAV[0,4]]]            
        elif self.CAV[0,7] == 20:
            CAV_prof += [[self.CAV[1,6] + self.CAV[2,6], self.CAV[2,4]]]                
        elif self.CAV[0,7] == 21:
            CAV_prof += [[self.CAV[2,6]*2, self.CAV[2,4]]]      
        
        return CAV_prof
                        
###############################################################################                
    # build the structure of the profile (composition on inner cell IC, end cell EC, pen cell PC, tube TU)  
    # depending on the number of the cells or on the code identifying your element. You can find more info
    # at the bottom of this file          
    def CAV_Prof(self):
        if self.Ncell < 16:
            CAV_PROF = []
            if self.l_cil_s != 0:
                CAV_PROF += ['TU']
            
            if self.Ncell == 1:
                CAV_PROF += ['ECs', 'ECd']
            elif self.Ncell == 2:
                CAV_PROF += ['ECs', 'PCd', 'PCs', 'ECd']
            else:
                CAV_PROF += ['ECs', 'PCd']+[ 'ICs', 'ICd']*(self.Ncell-2)+[ 'PCs', 'ECd']
            
            if self.l_cil_d != 0:
                CAV_PROF += ['TU']
        else:
            if self.Ncell == 16:
                CAV_PROF = ['ECd']
            elif self.Ncell == 17:
                CAV_PROF = ['PCd']
            elif self.Ncell == 18:
                CAV_PROF = ['ICd']
            elif self.Ncell == 19:
                if self.l_cil_s != 0:
                    CAV_PROF = ['TU', 'ECs']
                else:
                    CAV_PROF = ['ECs']
            elif self.Ncell == 20:
                CAV_PROF = ['PCd', 'ICs']
            elif self.Ncell == 21:
                CAV_PROF = ['ICd', 'ICs']
                
        return CAV_PROF
    
###############################################################################
 
    def half_cell_coo(self, cell_data, new_parameter):
        print('half cell coordinates')
        a = cell_data[0]
        b = cell_data[1]
        A = cell_data[2]
        B = cell_data[3]
        d_eq = cell_data[4]
        D_ir = cell_data[5]
        L = cell_data[6]

        new_parameter = new_parameter

        x0 = 0.0
        y0 = d_eq-b
        X0 = L
        Y0 = B+D_ir
        
        geom = Geometry()
        RP = geom.racc_point(cell_data)
        #RP = self.racc_point(cell_data)
        if np.any(np.isnan(RP)):
            return []
        elif RP.size == 0:
            return []
        else:
            # Disegno ellisse all'equatore
            # design of equator ellipse
            if a == b:
                EL1 = self.circ_arc(a, b, RP, x0, y0, 1)
            else:
                EL1 = self.ellipse_arc(a, b, RP, x0, y0, 1)
            EL1 = np.asarray([[0,y0+b]]+ EL1.tolist())

            # disegno ellisse all'iride
            # design of iris ellipse
            if A == B:
                EL2 = self.circ_arc(A, B, RP, X0, Y0, 2)
            else:
                EL2 = self.ellipse_arc(A, B, RP, X0, Y0, 2)
            EL2 = np.asarray(EL2.tolist() + [[L,Y0-B]])

            # disegno retta tangente
            # design of tangent
            l_r = ((RP[1,0]-RP[0,0])**2+(RP[1,1]-RP[0,1])**2)**0.5
            R = np.zeros((int(l_r/self.dx),2))
            R[:,0] = np.linspace(RP[0,0], RP[1,0], int(l_r/self.dx))
            R[:,1] = (RP[1,1]-RP[0,1])*(R[:,0]-RP[0,0])/(RP[1,0]-RP[0,0])+RP[0,1] 
            prof = np.append(EL1, R, axis=0) 
            prof = np.append(prof, EL2, axis=0) 

            #### new lines
            for i in range(len(prof)): # new line for new parameter by Elisa
                prof[i,0]+=self.new_parameter # new line for new parameter by Elisa

            prof = np.insert(prof,0,[0,EL1[0,1]],axis=0) # new line for new parameter by Elisa

            return prof
        
###############################################################################         
        
    def circ_arc(self, A, B, RP, X0, Y0, ellt): 
        if ellt == 1:
            alpha = np.arctan2(RP[0,1]-Y0, RP[0,0]-X0)
            beta = np.pi/2
        else:
            alpha = 2*np.pi + np.arctan2(RP[1,1]-Y0, RP[1,0]-X0)
            beta = 3*np.pi/2
            
        phi = np.linspace(0, 2*np.pi, int(2*np.pi*A/self.dx))
        ang = [x for x in phi if x > alpha and x < beta]
        EL = np.zeros((len(ang), 2))
        EL[:,0] = A*np.cos(ang) + X0
        EL[:,1] = B*np.sin(ang) + Y0
        
        if ellt == 1:
            EL = np.flip(EL,axis=0)
        
        return EL
            
############################################################################### 
            
    def ellipse_arc(self, A, B, RP, X0, Y0, ellt):
        if A < B:
            a = A
            b = B
            if ellt == 1:
                alpha = np.arccos((RP[0,0]-X0)/A)
                beta = np.pi/2
            else:
                alpha = 2*np.pi - np.arccos((RP[1,0]-X0)/A)
                beta = 3*np.pi/2
            ell = False
        elif A > B:
            a = B
            b = A
            if ellt == 1:
                alpha = np.arccos((RP[0,0]-X0)/A) + np.pi/2                
                beta = np.pi
            else:
                alpha = 2*np.pi - np.arccos((RP[1,0]-X0)/A) + np.pi/2
                beta = 2*np.pi
            ell = True
        
        
        
        h = (a-b)**2/(a+b)**2
        p = np.pi*(a+b)*(1+3*h/(10+(4-3*h)**0.5))
       
        phi = self.angles_in_ellipse(p/self.dx, a, b)             
        ang = [x for x in phi if x > alpha and x < beta]
               
        EL = np.zeros((len(ang),2))
        EL[:,0] = a*np.cos(ang) + X0
        EL[:,1] = b*np.sin(ang) + Y0
        
        if ellt == 1:
            EL = np.flip(EL,axis=0)
        
        if ell:
            EL_rot = np.zeros((len(EL),2))
            for k in range(len(EL)):
                EL_rot[k,0] = EL[k,1] - Y0 + X0
                EL_rot[k,1] = -EL[k,0] + X0 + Y0 
            return EL_rot            
        else:
            return EL
            
        
        
 


###############################################################################         
         
    def angles_in_ellipse(self, num, a, b):
        angles = 2 * np.pi * np.arange(num) / num
        if a != b:
            e = (1.0 - a ** 2.0 / b ** 2.0) ** 0.5
            tot_size = ellipeinc(2.0 * np.pi, e)
            arc_size = tot_size / num
            arcs = np.arange(num) * arc_size
            res = root(lambda x: (ellipeinc(x, e) - arcs), angles)
            angles = res.x 
        return angles     
    
##############################################################################
# Note:
# Ncell = 1 --> ECs+ECd==EG
# Ncell = 2 --> EC + PC == 2 cells cavity
# Ncell = 3 --> EC+IC+PC == 3 cells cavity

# Ncell = 16 --> half cell ECd
# Ncell = 17 --> half cell PCd
# Ncell = 18 --> half cell ICd


## pedix s == 'sinistra' == 'left'
## pedixd == 'destra' == 'right'