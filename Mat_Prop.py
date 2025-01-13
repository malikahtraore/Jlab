from os.path import normpath
import numpy as np
from os import getcwd
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QFileDialog, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon


Ui_MatProp, QtBaseClass = uic.loadUiType('mat_prop.ui')

class Mat_Prop(QDialog, Ui_MatProp):    
    def __init__(self, parent):
        super(Mat_Prop, self).__init__(parent)
        QWidget.__init__(self)
        Ui_MatProp.__init__(self)
        self.setupUi(self)
        
        #self.path = parent.path
        self.no_change = 'no'
        self.idx = []
        self.len_matps = 9
        mat_list = np.genfromtxt(getcwd() + '\\mat_prop.txt', dtype='str')

        self.name_list = []
        self.MATPs = []
        if len(np.shape(mat_list)) == 1:
            self.name_list += [str(mat_list[0])]
            self.MATPs += [[float(x) for x in mat_list[1:len(mat_list)]]] 
        else:
            for k in range(len(mat_list)):
                    self.name_list += [str(mat_list[k, 0])]
                    self.MATPs += [[float(x) for x in mat_list[k, 1:len(mat_list[0,:])]]]

            
        for item in self.name_list:
            self.list_material.addItem(item)
        
        self.list_material.itemSelectionChanged.connect(self.choosen_mat)
        
        self.pb_add.clicked.connect(self.add_new_material)
        self.pb_del.clicked.connect(self.delete_material)
        self.pb_import.clicked.connect(self.import_material)
        self.pb_OK.clicked.connect(self.press_OK)
        self.pb_cancel.clicked.connect(self.press_cancel)
        
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

##############################################################################
        # Logo
        
        MC_path = getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        
###############################################################################  
        
    def choosen_mat(self):
        if self.check_float() == False:
            self.list_material.blockSignals(True)
            self.list_material.setCurrentRow(self.idx)  
            self.list_material.blockSignals(False)
        elif self.no_change == 'no':
            if self.idx != []:
                self.MATPs[self.idx][0] = float(self.le_density.text())
                self.MATPs[self.idx][1] = float(self.le_E_rt.text())
                self.MATPs[self.idx][2] = float(self.le_E_cr.text())
                self.MATPs[self.idx][3] = float(self.le_pr_rt.text())
                self.MATPs[self.idx][4] = float(self.le_pr_cr.text())
                self.MATPs[self.idx][5] = float(self.le_Y.text())
                self.MATPs[self.idx][6] = float(self.le_rho_rt.text())
                self.MATPs[self.idx][7] = float(self.le_rho_cr.text())
                self.MATPs[self.idx][8] = float(self.le_alpha.text())
            
            self.idx = self.list_material.currentRow()
            self.le_density.setText(str(self.MATPs[self.idx][0]))
            self.le_E_rt.setText(str(self.MATPs[self.idx][1]))
            self.le_E_cr.setText(str(self.MATPs[self.idx][2]))
            self.le_pr_rt.setText(str(self.MATPs[self.idx][3]))
            self.le_pr_cr.setText(str(self.MATPs[self.idx][4]))
            self.le_Y.setText(str(self.MATPs[self.idx][5]))
            self.le_rho_rt.setText(str(self.MATPs[self.idx][6]))
            self.le_rho_cr.setText(str(self.MATPs[self.idx][7]))
            self.le_alpha.setText(str(self.MATPs[self.idx][8]))
            
###############################################################################  

    def set_mat_name(self):
        text, okPressed = QInputDialog.getText(self, "Add","New material name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
 
##############################################################################  

    def add_new_material(self):
        m_name = self.set_mat_name()
        
        self.name_list += [m_name]
        self.MATPs += [[0]*self.len_matps]
            
        self.list_material.addItem(m_name)   
        self.list_material.setCurrentRow(len(self.MATPs))  
                 
        self.le_density.setText('0.0')
        self.le_E_rt.setText('0.0')
        self.le_E_cr.setText('0.0')
        self.le_pr_rt.setText('0.0')
        self.le_pr_cr.setText('0.0')
        self.le_Y.setText('0.0')
        self.le_rho_rt.setText('0.0')
        self.le_rho_cr.setText('0.0')
        self.le_alpha.setText('0.0')

###############################################################################
    
    def delete_material(self):
        self.no_change = 'yes'
        self.name_list.remove(self.name_list[self.idx])
        self.MATPs.remove(self.MATPs[self.idx])
        self.idx = []
        
        self.le_density.setText('')
        self.le_E_rt.setText('')
        self.le_E_cr.setText('')
        self.le_pr_rt.setText('')
        self.le_pr_cr.setText('')
        self.le_Y.setText('')
        self.le_rho_rt.setText('')
        self.le_rho_cr.setText('')
        self.le_alpha.setText('')
        
        self.list_material.clear()
        for item in self.name_list:
            self.list_material.addItem(item)
        
        self.no_change = 'no'

###############################################################################
        
    def warning_already_exixst(self, n):
        reply = QMessageBox.question(
        self, "Warning",
        'Material ' + n + ' already exist, do you want to replace it?',
        QMessageBox.Ok | QMessageBox.Cancel)

        if reply == QMessageBox.Ok:
            return True
        else:
            return False

###############################################################################
        
    def import_material(self):
        path, _ = QFileDialog.getOpenFileName(self,"Import materials", "\home","Cavity database (*.txt)")
        i_mat_list = np.genfromtxt(normpath(str(path)), dtype='str')
            
        i_name_list = []
        i_MATPs = []
        for k in range(len(i_mat_list)):
            i_name_list += [str(i_mat_list[k, 0])]
            i_MATPs += [[float(x) for x in i_mat_list[k, 1:len(i_mat_list[0,:])]]]

        for k in range(len(i_name_list)):
            if i_name_list[k] in self.name_list:
                replace = self.warning_already_exixst(i_name_list[k])
                
                if replace:
                    lidx = self.name_list.index(i_name_list[k])
                    self.MATPs[lidx] = i_MATPs[k]
              
            else:
                self.list_material.addItem(i_name_list[k])       
                self.name_list += [i_name_list[k]]
                self.MATPs += [i_MATPs[k]]

        self.list_material.setCurrentRow(len(self.MATPs)-1) 

###############################################################################

    def warning_float(self, name):
        reply = QMessageBox.warning(
        self, "Warning",
        name + ' must be positive float number.',
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass

###############################################################################

    def check_float(self):
        data = [self.le_density.text(),
                self.le_density.text(),
                self.le_E_rt.text(),
                self.le_E_cr.text(),
                self.le_pr_rt.text(),
                self.le_pr_cr.text(),
                self.le_Y.text(),
                self.le_rho_rt.text(),
                self.le_rho_cr.text(),
                self.le_alpha.text()]
        
        name = ['Density',
                'Linear elastic modulus (room temperature)',
                'Linear elastic modulus (criogenic)',
                'Poisson ratio (room temperature)',
                'Poisson ratio (criogenic)',
                'Yeld limit',
                'Resistivity (room temperature)',
                'Resistivity (criogenic)',
                'Thermal expansion coefficient']
       
        if all(flag == '' for (flag) in data):
            return True
        else:
            for k in range(len(data)):
                try:
                    if float(data[k]) >= 0:
                        ok = 1
                except:
                    self.warning_float(name[k])
                    ok = 0
                    break
                
            if ok == 1:
                return True
            else:
                return False

###############################################################################
        
    def press_OK(self):
        if self.check_float():
            try:
                self.MATPs[self.idx][0] = float(self.le_density.text())
                self.MATPs[self.idx][1] = float(self.le_E_rt.text())
                self.MATPs[self.idx][2] = float(self.le_E_cr.text())
                self.MATPs[self.idx][3] = float(self.le_pr_rt.text())
                self.MATPs[self.idx][4] = float(self.le_pr_cr.text())
                self.MATPs[self.idx][5] = float(self.le_Y.text())
                self.MATPs[self.idx][6] = float(self.le_rho_rt.text())
                self.MATPs[self.idx][7] = float(self.le_rho_cr.text())
                self.MATPs[self.idx][8] = float(self.le_alpha.text())
            except:
                pass
            export_mat = []
            for k in range(len(self.name_list)):
                export_mat += [[self.name_list[k]] + self.MATPs[k]]
            np.savetxt(getcwd() + '\\mat_prop.txt', np.asarray(export_mat), delimiter=" ", fmt="%s")
            self.mat_idx = self.idx
            self.close()

###############################################################################
        
    def press_cancel(self):
        self.close()