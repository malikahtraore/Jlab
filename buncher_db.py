# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:49:54 2022

@author: edelcore
"""

import os
from os.path import normpath
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QHeaderView, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5 import uic,  QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QTableWidgetItem,QVBoxLayout

#from Draw_cavity_profile import Draw_cavity_profile
#from D2P_par import D2P_par

dbui, QtBaseClass = uic.loadUiType('buncher_db.ui')

class buncher_db(QDialog, dbui):    
    def __init__(self, parent):
        super(buncher_db, self).__init__(parent)
        QWidget.__init__(self)
        dbui.__init__(self)
        self.setupUi(self)
        
        self.le_f_4 = parent.le_f_4
        self.le_bt_r = parent.le_bt_r
        self.le_bt_l = parent.le_bt_l
        self.le_l = parent.le_l
        self.le_m = parent.le_m
        self.le_u = parent.le_u
        self.le_gap = parent.le_gap
        self.le_sh = parent.le_sh
        self.le_l_m = parent.le_l_m
        self.le_angle = parent.le_angle
        self.le_beta_4 = parent.le_beta_4

        self.path_to_elmg_file=parent.path_to_elmg_file
        self.pathDB=''
        self.file_name=''
        self.path_project = parent.path_project
        self.row=[]
        
        self.db_OK.clicked.connect(self.button_ok)
        self.db_cancel.clicked.connect(self.button_cancel)  
        self.db_addData.clicked.connect(self.button_addData)
        
        self.db_view.clicked.connect(self.button_view)
        self.pushButton_Delete.clicked.connect(self.button_Delete)
        
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
 
        self.vBox = QVBoxLayout()
        self.setLayout(self.vBox)
        
        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.tableWidget.setStyleSheet("""
        QTableWidget {
                border: 2px solid grey;
                border-radius: 10px;
                gridline-color: grey;
                background-color: #f0f0f0;
            }
        QTableWidget::item {
                padding: 5px;
            }
        QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }      
        QHeaderView::section {
                background-color: lightblue;
                color: white;
                border: 1px solid #005a9e;
                padding: 4px;
                font-weight: bold;
            }                                                                        
        """)
            
        try:
            self.button_import_automatic()
        except:
            self.warning_wdj('Errors opening the DB')

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\buncher.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)

###############################################################################

    def button_import_automatic(self):
        try:
            try:
                self.pathDB = self.path_project+'\\DB_file'
                files = os.listdir(self.pathDB)
                if len(files)!=0:
                    self.file_name=files[0]
                else:
                    self.file_name='dbfile.txt'
                    file=open(self.pathDB+'\\dbfile.txt','w')
                    file.close()
                self.pathDB+='\\'+self.file_name
                    
                ok = 1
            except:
                ok=0        
    
            #load the file
            if ok == 1 and self.pathDB!='.':
                filedb=open(self.pathDB, 'r')
                read=filedb.readlines()
                filedb.close()
                
                while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)
                rowPosition = self.tableWidget.rowCount()
                for i in range(len(read)):
                    line=read[i].split(';')
                    if str(line[0]).__contains__('B'):
                        self.tableWidget.insertRow(rowPosition)
                        self.tableWidget.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                        self.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                        self.tableWidget.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                        self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                        self.tableWidget.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                        self.tableWidget.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                        self.tableWidget.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                        self.tableWidget.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                        self.tableWidget.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                        self.tableWidget.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                        self.tableWidget.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                        self.tableWidget.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                        cell_item=self.tableWidget.item(rowPosition, 1)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 2)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 3)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 4)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 5)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 6)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 7)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 8)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 9)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 10)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 11)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
        except:
            self.warning_wdj('Import failed. Retry')          
##############################################################################

    def button_ok(self):        
        try:
            fileEG=open(self.pathDB,'r')
            lineeEG=fileEG.readlines()
            fileEG.close()
            EG=[]
            for i in range(len(lineeEG)):
                if lineeEG[i].startswith('EG') or lineeEG[i].startswith('SC') or lineeEG[i].startswith('B'):
                    EG.append(lineeEG[i])
            
            numberRows=self.tableWidget.rowCount()
            a=[]
            for row in range(numberRows):
                a.append('B;')
                for col in range(12):
                    if col!=11:
                        a.append(self.tableWidget.item(row, col).text()+';')
                    else:
                        a.append(self.tableWidget.item(row, col).text())
                if row!=numberRows-1:
                    a.append('\n')
            filedb=open(self.pathDB,'w')
            for i in range(len(a)):
                filedb.writelines(a[i])
            for i in range(len(EG)):
                if i==0:
                    filedb.writelines('\n'+EG[i])
                else:
                    filedb.writelines(EG[i])
            filedb.close()        
            self.close()
        except:
            self.close()
            
        try:
            fileDB=open(self.pathDB,'r')
            lineeDB=fileDB.readlines()
            fileDB.close()
            l=[]
            for i in range(len(lineeDB)):
                if lineeDB[i].startswith('EG') or lineeDB[i].startswith('HC') or lineeDB[i].startswith('SC') or lineeDB[i].startswith('B'):
                    l.append(lineeDB[i])
            fileDB=open(self.pathDB,'w')
            lineeDB=fileDB.writelines(l)
            fileDB.close()
        except:
            self.warning_wdj('Some errors writing the db file')
            
##############################################################################   
                    
    def button_cancel(self):
        self.close()

##############################################################################

    def button_addData(self):
        
        param=True
        try:
            if not isinstance(float(self.le_f_4.text()), float):
                self.warning_wdj('Frequency must be a number')
                param=False
        except:
            self.warning_wdj('Frequency must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_bt_r.text()), float):
                self.warning_wdj('Beam pipe radius must be a number')
                param=False
        except:
            self.warning_wdj('Beam pipe radius must be a number')
            param=False
        
        try:
            if not isinstance(float(self.le_bt_l.text()), float):
                self.warning_wdj('Beam pipe length must be a number')
                param=False
        except:
            self.warning_wdj('Beam pipe length must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_l.text()), float):
                self.warning_wdj('Iris radius must be a number')
                param=False
        except:
            self.warning_wdj('Iris radius must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_m.text()), float):
                self.warning_wdj('Medium radius must be a number')
                param=False
        except:
            self.warning_wdj('Medium radius must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_u.text()), float):
                self.warning_wdj('Dome radius must be a number')
                param=False
        except:
            self.warning_wdj('Dome radius must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_gap.text()), float):
                self.warning_wdj('Gap must be a number')
                param=False
        except:
            self.warning_wdj('Gap must be a number')
            param=False
        
        try:
            if not isinstance(float(self.le_sh.text()), float):
                self.warning_wdj('Sh must be a number')
                param=False
        except:
            self.warning_wdj('Sh must be a number')
            param=False

        try:
            if not isinstance(float(self.le_l_m.text()), float):
                self.warning_wdj('l_m must be a number')
                param=False
        except:
            self.warning_wdj('l_m must be a number')
            param=False      

        try:
            if not isinstance(float(self.le_angle.text()), float):
                self.warning_wdj('b_angle must be a number')
                param=False
        except:
            self.warning_wdj('b_angle must be a number')
            param=False  

        try:
            if not isinstance(float(self.le_beta_4.text()), float):
                self.warning_wdj('beta must be a number')
                param=False
        except:
            self.warning_wdj('beta must be a number')
            param=False              
  
        if not param:
            print(param)
        else:    
            self.row.append(self.le_f_4.text())
            self.row.append(self.le_bt_r.text())
            self.row.append(self.le_bt_l.text())
            self.row.append(self.le_l.text())
            self.row.append(self.le_m.text())
            self.row.append(self.le_u.text())
            self.row.append(self.le_gap.text())
            self.row.append(self.le_sh.text())
            self.row.append(self.le_l_m.text())
            self.row.append(self.le_angle.text())
            self.row.append(self.le_beta_4.text())
                        
            rowPosition = self.tableWidget.rowCount()
          
            cellName = self.te_i2.toPlainText()
            
            arrayName=[]
            if os.path.exists(self.pathDB)==True:
                file0=open(self.pathDB, "r")
                ll=file0.readlines()
                file0.close()
                for i in range(len(ll)):
                    lsplit=ll[i].split(';')
                    if lsplit[0]=='B':
                        arrayName.append(lsplit[0])
            
            if cellName == '':
                self.warning_wdj('Cell Name cannot be empty')
            else:
                cont=0
                for i in range(len(arrayName)):
                    if arrayName[i]==cellName:
                        self.warning_wdj('Please insert another cell name')
                        break
                    else:
                       cont+=1
                       
                if cont==len(arrayName):
                    #### add to tableWidget the new line  self.SF_param[5]
                    self.tableWidget.insertRow(rowPosition)
                    self.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(str(self.row[0])))
                    self.tableWidget.setItem(rowPosition , 2, QTableWidgetItem(str(self.row[1])))
                    self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem(str(self.row[2])))
                    self.tableWidget.setItem(rowPosition , 4, QTableWidgetItem(str(self.row[3])))
                    self.tableWidget.setItem(rowPosition , 5, QTableWidgetItem(str(self.row[4])))
                    self.tableWidget.setItem(rowPosition , 6, QTableWidgetItem(str(self.row[5])))
                    self.tableWidget.setItem(rowPosition , 7, QTableWidgetItem(str(self.row[6])))
                    self.tableWidget.setItem(rowPosition , 8, QTableWidgetItem(str(self.row[7])))
                    self.tableWidget.setItem(rowPosition , 9, QTableWidgetItem(str(self.row[8])))
                    self.tableWidget.setItem(rowPosition , 11, QTableWidgetItem(str(self.row[10])))
                    self.tableWidget.setItem(rowPosition , 0 , QTableWidgetItem(cellName))
                    self.tableWidget.setItem(rowPosition , 10, QTableWidgetItem(str(self.row[9])))
                    cell_item=self.tableWidget.item(rowPosition, 1)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 2)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 3)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 4)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 5)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 6)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 7)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 8)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 9)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 10)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 11)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)


##############################################################################
    # select row of desired data to simulate
    
    def button_view(self):
        try:
            cont=0
            if QtCore.Qt.LeftButton:
                current_row = self.tableWidget.currentRow()
                cont+=1
                
            if cont==1:
                row1=[]
                try:
                    current_row = self.tableWidget.currentRow()
                    for i in range(12):
                        row1.append(self.tableWidget.item(current_row, i).text())
                except:
                    self.warning_wdj('no row selected')
                
            if cont>0:
                self.le_f_4.setText(row1[1])
                self.le_beta_4.setText(row1[11])
                self.le_bt_r.setText(row1[2])
                self.le_bt_l.setText(row1[3])
                self.le_l.setText(row1[4])
                self.le_m.setText(row1[5])
                self.le_u.setText(row1[6])
                self.le_gap.setText(row1[7])
                self.le_sh.setText(row1[8])
                self.le_l_m.setText(row1[9])
                self.le_angle.setText(row1[10])
            self.close()
            return(row1)
        except:
            self.warning_wdj('Something goes wrong. Retry')      

###############################################################################

    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass 

##############################################################################
        
    def delete_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Yes, QMessageBox.No)

        return reply
    
##############################################################################
    
    def button_Delete(self):
        reply=self.delete_wdj('Are you sure you want to delete the row?')
        if reply == QMessageBox.Yes:
            if QtCore.Qt.LeftButton:
                current_row = self.tableWidget.currentRow()
                self.tableWidget.removeRow(current_row)
        else:
            pass