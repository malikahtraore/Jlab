# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:49:54 2022

@author: edelcore
Half cell database
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

dbui, QtBaseClass = uic.loadUiType('db2.ui')

class DB(QDialog, dbui):    
    def __init__(self, parent):
        super(DB, self).__init__(parent)
        QWidget.__init__(self)
        dbui.__init__(self)
        self.setupUi(self)
        
        self.path_to_elmg_file=parent.path_to_elmg_file
        self.SF_param = parent.SF_param
        self.CAV_ge = parent.CAV_ge
        self.CAV_py = parent.CAV_py
        self.CELL = parent.CELL
        self.le_f = parent.le_f
        self.le_Sxeq = parent.le_Sxeq
        self.le_Syeq = parent.le_Syeq
        self.le_Sxir = parent.le_Sxir
        self.le_Syir = parent.le_Syir
        self.le_ER = parent.le_ER
        self.le_IR = parent.le_IR
        self.le_SL = parent.le_SL
        self.le_beta = parent.le_beta
        self.le_LEQ = parent.le_LEQ    #Modified by Malini
        self.pathDB=''
        self.file_name=''
        self.path_project = parent.path_project
        self.row=[]
        
        self.db_OK.clicked.connect(self.button_ok)
        self.db_cancel.clicked.connect(self.button_cancel)  
        self.db_addData.clicked.connect(self.button_addData)
        self.db_import.clicked.connect(self.button_import)
        
        self.db_view.clicked.connect(self.button_view)
        self.pushButton_GetEG.clicked.connect(self.button_getEG)
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

        if self.le_f.text().__contains__('0') or self.le_f.text().__contains__('1') or self.le_f.text().__contains__('2') or self.le_f.text().__contains__('3') or self.le_f.text().__contains__('4') or self.le_f.text().__contains__('5') or self.le_f.text().__contains__('6') or self.le_f.text().__contains__('7') or self.le_f.text().__contains__('8') or self.le_f.text().__contains__('9') or self.le_f.text().__contains__('10'):
            self.pushButton_GetEG.setEnabled(True)
        else:
            self.pushButton_GetEG.setEnabled(False)
            
        try:
            self.button_import_automatic()
        except:
            self.warning_wdj('Errors opening the DB')

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
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
                    if str(line[0]).__contains__('HC'):
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
                        self.tableWidget.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                        self.tableWidget.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                        self.tableWidget.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                        self.tableWidget.setItem(rowPosition , 15, QTableWidgetItem(str(line[16]))) #Modified by Malini
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
                        cell_item=self.tableWidget.item(rowPosition, 12)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 13)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 14)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 15)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable) #Modified by Malini 
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
                a.append('HC;')
                for col in range(16):
                    if col!=15:
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
                if lineeDB[i].startswith('EG') or lineeDB[i].startswith('HC') or lineeDB[i].startswith('SC') or lineeEG[i].startswith('B'):
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
            if not isinstance(float(self.le_f.text()), float):
                self.warning_wdj('Frequency must be a number')
                param=False
        except:
            self.warning_wdj('Frequency must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_Sxeq.text()), float):
                self.warning_wdj('Sxeq must be a number')
                param=False
        except:
            self.warning_wdj('Sxeq must be a number')
            param=False
        
        try:
            if not isinstance(float(self.le_Syeq.text()), float):
                self.warning_wdj('Syeq must be a number')
                param=False
        except:
            self.warning_wdj('Syeq must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_Sxir.text()), float):
                self.warning_wdj('Sxir must be a number')
                param=False
        except:
            self.warning_wdj('Sxir must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_Syir.text()), float):
                self.warning_wdj('Syir must be a number')
                param=False
        except:
            self.warning_wdj('Syir must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_ER.text()), float):
                self.warning_wdj('ER must be a number')
                param=False
        except:
            self.warning_wdj('ER must be a number')
            param=False
            
        try:
            if not isinstance(float(self.le_IR.text()), float):
                self.warning_wdj('IR must be a number')
                param=False
        except:
            self.warning_wdj('IR must be a number')
            param=False
        
        try:
            if not isinstance(float(self.le_SL.text()), float):
                self.warning_wdj('SL must be a number')
                param=False
        except:
            self.warning_wdj('SL must be a number')
            param=False

        try:
            if not isinstance(float(self.le_LEQ.text()), float):
                self.warning_wdj('LEQ must be a number')
                param=False
        except:
            self.warning_wdj('LEQ must be a number')
            param=False                                    #Modified by Malini
  
        if not param:
            print(param)
        else:    
            self.row.append(self.le_f.text())
            self.row.append(self.le_Sxeq.text())
            self.row.append(self.le_Syeq.text())
            self.row.append(self.le_Sxir.text())
            self.row.append(self.le_Syir.text())
            self.row.append(self.le_ER.text())
            self.row.append(self.le_IR.text())
            self.row.append(self.le_SL.text())
            self.row.append(self.le_LEQ.text())

                  #Modified by Malini
            
            HpeakEacc=round(float(self.SF_param[6])*0.0012566370614359172/10,2)
            
            rowPosition = self.tableWidget.rowCount()
          
            cellName = self.te_i2.toPlainText()
            
            arrayName=[]
            if os.path.exists(self.pathDB)==True:
                file0=open(self.pathDB, "r")
                ll=file0.readlines()
                file0.close()
                for i in range(len(ll)):
                    lsplit=ll[i].split(';')
                    if lsplit[0]=='HC':
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
                    self.tableWidget.setItem(rowPosition , 9, QTableWidgetItem(str(self.SF_param[8])))
                    self.tableWidget.setItem(rowPosition , 11, QTableWidgetItem(str(round(float(self.SF_param[5])/10,2))))
                    self.tableWidget.setItem(rowPosition , 12, QTableWidgetItem(str(HpeakEacc)))
                    self.tableWidget.setItem(rowPosition , 13, QTableWidgetItem(str(self.SF_param[3])))
                    self.tableWidget.setItem(rowPosition , 14, QTableWidgetItem(str(self.SF_param[2])))
                    self.tableWidget.setItem(rowPosition , 15, QTableWidgetItem(str(self.SF_param[7])))
                    self.tableWidget.setItem(rowPosition , 0 , QTableWidgetItem(cellName))
                    self.tableWidget.setItem(rowPosition , 10, QTableWidgetItem(str(self.row[8])))
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
                    cell_item=self.tableWidget.item(rowPosition, 12)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 13)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 14)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget.item(rowPosition, 15)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)   #Modified by Malini
                                            
                                        
                                        
            
###############################################################################

    def button_import(self):
        try:
            try:
                self.pathDB, _ = QFileDialog.getOpenFileName(self,"Import DB", "\\home", "*.txt")
                
                self.pathDB = normpath(str(self.pathDB))
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
                    if str(line[0]).__contains__('HC'):
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
                        self.tableWidget.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                        self.tableWidget.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                        self.tableWidget.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                        self.tableWidget.setItem(rowPosition , 15, QTableWidgetItem(str(line[16]))) #Modified by Malini
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
                        cell_item=self.tableWidget.item(rowPosition, 12)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 13)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.tableWidget.item(rowPosition, 14)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item-self.tableWidget.item(rowPosition, 15)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)        #Modified by Malini
        except:
            self.warning_wdj('Import failed. Retry')               
            
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
                    for i in range(15):
                        row1.append(self.tableWidget.item(current_row, i).text())
                except:
                    self.warning_wdj('no row selected')
                
            if cont>0:
                self.le_f.setText(row1[1])
                self.le_beta.setText(row1[9])#2
                self.le_Sxeq.setText(row1[2])#8
                self.le_Syeq.setText(row1[3])#9
                self.le_Sxir.setText(row1[4])#10
                self.le_Syir.setText(row1[5])#11
                self.le_ER.setText(row1[6])#12
                self.le_IR.setText(row1[7])#13
                self.le_SL.setText(row1[8])#14
                self.le_LEQ.setText(row1[10])
            self.close()
            return(row1)
        except:
            self.warning_wdj('Something goes wrong. Retry')
        # try:
        #     row=[]
        #     dati=False
        #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
        #        dati=True
        #        row.append(currentQTableWidgetItem.text())
             
        #     if len(row)==1:
        #         row=[]
        #     #### Select a cell
        #         current_row = self.tableWidget.currentRow()
        #         for i in range(15):
        #             row.append(self.tableWidget.item(current_row, i).text())
            
        #     # modify data to write
        #     self.SF_param[0] = row[0]
        #     self.CELL[0] = row[1]
        #     self.CELL[1] = row[2]
        #     self.CELL[2] = row[3]
        #     self.CELL[3] = row[4]
        #     self.CELL[4] = row[5]
        #     self.CELL[5] = row[6]
        #     self.CELL[6] = row[7]
        #     self.SF_param[8] = row[8]
        #     self.SF_param[5] = row[9]
        #     HpeakEacc = row[10]
        #     self.SF_param[6]=float(HpeakEacc)*10/0.0012566370614359172
        #     self.SF_param[3] = row[11]
        #     self.SF_param[2] = row[12]
        #     self.SF_param[7] = row[13]
        #     self.le_f.setText(row[1])
        #     self.le_Sxeq.setText(row[2])
        #     self.le_Syeq.setText(row[3])
        #     self.le_Sxir.setText(row[4])
        #     self.le_Syir.setText(row[5])
        #     self.le_ER.setText(row[6])
        #     self.le_IR.setText(row[7])
        #     self.le_SL.setText(row[8])
        #     self.le_beta.setText(row[9])
        
        #     file = open(os.getcwd()+'\\selectRow.txt','w')
        #     file.writelines(row[0]+';'+row[1]+';'+row[2]+';'+row[3]+';'+row[4]+';'+row[5]+';'+row[6]+';'+row[7]+';'+row[8]+';'+row[9])
        #     file.close()
        # except:
        #     #if dati==False:
        #     self.warning_wdj('Select a row')

###############################################################################

    def check(self):
        
        self.frame_i2.show()
        if os.path.exists(os.getcwd()+"\\CellDb.txt")==True: 
            
            file4=open(os.getcwd()+"\\CellDb.txt",'r') # first line control
            read=file4.readlines()
            file4.close()
            file41=open(os.getcwd()+"\\CellDb.txt",'w')
            if len(read) > 0:
                if read[0]=='\n':
                    for i in range(1, len(read)):
                        file41.writelines(read[i])
                else:
                    for i in range(0, len(read)):
                        file41.writelines(read[i]) 
                file41.close()
            
            try:
                fileDb=open(os.getcwd()+"\\CellDb.txt")
                line=fileDb.readlines()
#                numberLines=len(line)
                fileDb.close()
                try:
                    while (self.tableWidget.rowCount() > 0):
                        self.tableWidget.removeRow(0)
                    rowPosition = self.tableWidget.rowCount()
                    if len(line) !=0: ## add to tableWidget all the data saved in the txt db
                         for i in range(len(line)):
                                 self.tableWidget.insertRow(rowPosition)
                                 lineAdd=line[i].split(";")
                                 self.tableWidget.setItem(rowPosition , 1, QTableWidgetItem(str(lineAdd[0])))
                                 self.tableWidget.setItem(rowPosition , 2, QTableWidgetItem(str(lineAdd[1])))
                                 self.tableWidget.setItem(rowPosition , 3, QTableWidgetItem(str(lineAdd[2])))
                                 self.tableWidget.setItem(rowPosition , 4, QTableWidgetItem(str(lineAdd[3])))
                                 self.tableWidget.setItem(rowPosition , 5, QTableWidgetItem(str(lineAdd[4])))
                                 self.tableWidget.setItem(rowPosition , 6, QTableWidgetItem(str(lineAdd[5])))
                                 self.tableWidget.setItem(rowPosition , 7, QTableWidgetItem(str(lineAdd[6])))
                                 self.tableWidget.setItem(rowPosition , 8, QTableWidgetItem(str(lineAdd[7])))
                                 self.tableWidget.setItem(rowPosition , 9, QTableWidgetItem(str(lineAdd[8])))
                                 self.tableWidget.setItem(rowPosition , 10, QTableWidgetItem(str(lineAdd[9])))
                                 self.tableWidget.setItem(rowPosition , 11, QTableWidgetItem(str(lineAdd[10])))
                                 self.tableWidget.setItem(rowPosition , 12, QTableWidgetItem(str(lineAdd[11])))
                                 self.tableWidget.setItem(rowPosition , 13, QTableWidgetItem(str(lineAdd[12])))
                                 self.tableWidget.setItem(rowPosition , 14, QTableWidgetItem(str(lineAdd[13])))
                                 self.tableWidget.setItem(rowPosition , 0, QTableWidgetItem(str(lineAdd[14])))
                                 self.tableWidget.setItem(rowPosition , 15, QTableWidgetItem(str(lineAdd[15])))  #Modified by Malini
                    return 'Inner Cell'
                except:
                    self.warning_wdj('Unable to add db data to tableWidget')
            except:
                self.warning_wdj('Unable to open file cavityDb.txt') 
            
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
    
    def button_getEG(self):
        try:
            if self.te_i2.toPlainText() != '':
                cellName=self.te_i2.toPlainText()
                
                try:
                    self.pathDB, _ = QFileDialog.getSaveFileName(self,"Save DB", "\\home", "*.txt")
                    
                    self.pathDB = normpath(str(self.pathDB))
                    ok = 1
                except:
                    ok=0
                
                if ok == 1:
                    filedb=open(self.pathDB, 'w')
                    numberRows=self.tableWidget.rowCount()
                    a=[]
                    for row in range(numberRows):
                        a.append('HC;')
                        for col in range(15):
                            if col==14:
                                a.append(self.tableWidget.item(row, col).text()+'\n')
                            else:
                                a.append(self.tableWidget.item(row, col).text()+';')
                        # if row!=numberRows-1:
                        #     a.append('\n')
                    filedb.writelines(a)
                    filedb.close() 
                
            else:
                self.warning_wdj('Please insert a valid cell name')
                
        except:
            self.warning_wdj('Saving Failed. Retry')

##############################################################################
    
    def button_Delete(self):
        reply=self.delete_wdj('Are you sure you want to delete the row?')
        if reply == QMessageBox.Yes:
            if QtCore.Qt.LeftButton:
                current_row = self.tableWidget.currentRow()
                self.tableWidget.removeRow(current_row)
        else:
            pass
        
##############################################################################
        
    def accessDB(self, path):
        try:
            file=open(path,'r')
            
            file.close()
        except:
            self.warning_wdj('Please insert a valid file. NB: access file version previous to 2013 year are not valid')
        
