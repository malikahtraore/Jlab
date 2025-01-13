# Geometry functions for cavity profile description
'''
- Conversion from geometric to physics parameters
- Conversion from physics to geometric parameters

#- Definition of ellipses tangent points
#- Calculation of the slope of the tangent line to an ellipse 
#passing through a point and the point of tangency
#- Calculation of the points of intersection between a line and 
#an ellipse

'''

import numpy as np

class Geometry():

    def __init__(self):
        self.description='geometry'

    # physic to geometric parameters conversion
    def p2g_geom(self,R_ir,alpha,R,r,d,L,H):
        m = np.tan(3*np.pi/2+alpha)
        a1 = m**2
        b1 = m*((r**2+m**2)*(d-L)-m**2*(d-L)+L*r**2)
        c1 = (m**2*(d-L)-L*r**2)**2-(r**2+m**2)*(L**2*r**2+m**2*(d-L)**2)
        
        b = (-b1+np.sqrt(b1**2-a1*c1))/a1
        a = b/r
                
        Y0 = R_ir + b + H
        a4 = R**2+m**2
        b4 = m*(m*(d-L)+R_ir-Y0)
        #c4 = (m*(d-L)+R_ir-Y0)**2-B**2
        B = np.sqrt((m*(d-L)+R_ir-Y0)**2 - b4**2/a4)
        A = B/R
        R_eq = Y0 + B
        return A, B, a, b, R_eq
    
    # geometric to physic parameters conversion
    def g2p_geom(self, CAV):
        XYP = self.racc_point(CAV)
        A = CAV[0]
        B = CAV[1]
        a = CAV[2]
        b = CAV[3]
        R_eq = CAV[4]
        R_ir = CAV[5]       
        L = CAV[6]
        r = b/a
        R = B/A
        H = (R_eq-B)-(R_ir+b)
        alpha = (np.arctan2(XYP[1,0]-XYP[0,0],XYP[0,1]-XYP[1,1]))*180/np.pi
        m = (XYP[0,1]-XYP[1,1])/(XYP[0,0]-XYP[1,0])
        d = L - (R_ir-XYP[1,1])/m - XYP[1,0]
        return R_ir, alpha, R, r, d, L, H

##############################################################################           
############################################################################## 
##############################################################################
# Definition of ellipses tangent points 

    def racc_point(self, cell_data):
        b_eq = cell_data[0]
        a_eq = cell_data[1]
        b_ir = cell_data[2]
        a_ir = cell_data[3]
        d_eq = cell_data[4]
        D_ir = cell_data[5]
        L = cell_data[6]
        
        yc_eq = 0.0
        xc_eq = d_eq - cell_data[1]
        yc_ir = L
        xc_ir = cell_data[3] + D_ir
        
        if xc_eq - a_eq == xc_ir - a_ir:
            xc_eq += 0.001
            
        #try:
        ang_0 = 180*np.pi/180
        ang_1 = 360*np.pi/180
        x_p0 = a_ir*np.cos(ang_0) + xc_ir
        y_p0 = b_ir*np.sin(ang_0) + yc_ir
        m_0, xt_eq, yt_eq = self.point_ell_up(a_eq, b_eq, xc_eq, yc_eq, x_p0, y_p0)
        dist_0 = self.def_dist(a_ir, b_ir, xc_ir, yc_ir, xt_eq, yt_eq, m_0, x_p0, y_p0)
        
        x_p1 = a_ir*np.cos(ang_1) + xc_ir
        y_p1 = b_ir*np.sin(ang_1) + yc_ir
        m_1, xt_eq, yt_eq = self.point_ell_up(a_eq, b_eq, xc_eq, yc_eq, x_p1, y_p1)
        dist_1 = self.def_dist(a_ir, b_ir, xc_ir, yc_ir, xt_eq, yt_eq, m_1, x_p1, y_p1)   
        
        n = 0
        while True:
            ang_3 = (ang_0 + ang_1)/2
            x_p3 = a_ir*np.cos(ang_3) + xc_ir
            y_p3 = b_ir*np.sin(ang_3) + yc_ir
            m_3, xt_eq, yt_eq = self.point_ell_up(a_eq, b_eq, xc_eq, yc_eq, x_p3, y_p3)
            dist_3 = self.def_dist(a_ir, b_ir, xc_ir, yc_ir, xt_eq, yt_eq, m_3, x_p3, y_p3) 
        
            if dist_3 < 1e-5 or n == 100:
                POINT = np.asarray([[yt_eq, xt_eq],[y_p3, x_p3]])
                return POINT
                break
            elif dist_0 < dist_1:
                dist_1 = dist_3
                ang_1 = ang_3  
            else:
                dist_0 = dist_3
                ang_0 = ang_3  
            n = n+1

    def point_ell_up(self, a, b, C, D, E, F):
        # Calculation of the slope of the tangent line to an ellipse passing through a point and the
        # point of tangency
        A = (1/a)**2
        B = (1/b)**2
        G = B*(F-D)**2 + A*C**2 - 1 
        M2 = B*(B*(F-D)**2 + 2*A*C*E - A*E**2 - G)
        M1 = A*B*(E-C)*(F-D)
        M0 = A*(A*C**2 - G)
        
        if M1**2-M2*M0 < 0 or M2 == 0:
            return 'err'
        else: 
            m1 = (-M1-np.sqrt(M1**2-M2*M0))/M2
            m2 = (-M1+np.sqrt(M1**2-M2*M0))/M2
        
        X2 = A + B*m1**2
        X1 = -(A*C + B*E*m1**2 + B*(D-F)*m1)  
        x = -X1/X2
        y = m1*(x-E) + F
        if y > D:
            m = m1
        else:
            m = m2
            X2 = A + B*m**2
            X1 = -(A*C + B*E*m**2 + B*(D-F)*m)    
            x = -X1/X2    
            y = m*(x-E) + F
    
        return m, x, y
    
    def def_dist(self, a, b, C, D, E, F, m, x, y):
        # Calculation of the points of intersaction between a line and an ellipse
        A = (1/a)**2
        B = (1/b)**2    
        G = A + B*m**2
        H = A*C + B*D*m
        I = A*C**2 + B*D**2 - 1
        Q2 = B**2 * m**2 - G*B
        Q1 = G*B*D - H*B*m
        Q0 = H**2 - G*I
        q = (-Q1 + np.sqrt(Q1**2 - Q0*Q2))/Q2  
        
        if m*((H - B*m*q)/G) + q > D:
            q = (-Q1 - np.sqrt(Q1**2 - Q0*Q2))/Q2   
            
        dist = abs(y - (m*x + q))/np.sqrt(1 + m**2)
        
        return dist 