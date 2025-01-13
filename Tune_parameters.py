from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5 import uic
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon


Ui_Tune_parameters, QtBaseClass = uic.loadUiType('Tune_parameters.ui')

class Tune_parameters(QDialog, Ui_Tune_parameters):
    def __init__(self, parent=None):
        super(Tune_parameters, self).__init__(parent)
        QMainWindow.__init__(self)
        Ui_Tune_parameters.__init__(self)
        self.setupUi(self)
        
        self.pb_OK.clicked.connect(self.button_ok)
        self.pb_cancel.clicked.connect(self.button_cancel)
        
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        
############################################################################## 
        
    def button_ok(self): #retrieves tuning acuracy from f_toll, input can only be positive decimals 
        try:
            self.f_toll = float(self.le_f_toll.text())
            if self.f_toll < 0:
                self.wdj_warning('Tuning accuracy must be positive float numbers!')
            else:
                self.close()           
        except: #triggerd when input doesn't meet the requirements 
            self.wdj_warning('Tuning accuracy must be positive float numbers!')
            
##############################################################################            
            
    def button_cancel(self):
        self.f_toll = 'cancel'
        self.close()
            
##############################################################################
        
    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass  
        
##############################################################################