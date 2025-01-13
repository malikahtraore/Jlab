# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:27:46 2022

@author: edelcore

#### 23 07 2024: add the new parameter management: equator length
For the End Group Window
"""

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import os
from os.path import normpath
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem

ECui, QtBaseClass = uic.loadUiType('EndCell.ui')

class EndCell(QDialog, ECui):    
    def __init__(self, parent):
        super(EndCell, self).__init__(parent)
        QWidget.__init__(self)
        ECui.__init__(self)
        self.setupUi(self)
        
        self.pb_OK.clicked.connect(self.button_ok)
        self.pb_cancel.clicked.connect(self.button_cancel)
        self.db_import.clicked.connect(self.button_import)
        self.pathDB=''
        
        self.TW.verticalHeader().setVisible(False) # to disable the vertical header
        
        self.path_to_elmg_file=parent.path_to_elmg_file
        self.le_f=parent.le_f
        
        self.le_Sxeq_IC=parent.le_Sxeq_IC
        self.le_Syeq_IC=parent.le_Syeq_IC
        self.le_Sxir_IC=parent.le_Sxir_IC
        self.le_Syir_IC=parent.le_Syir_IC
        self.le_ER_IC=parent.le_ER_IC
        self.le_IR_IC=parent.le_IR_IC
        self.le_SL_IC=parent.le_SL_IC
        self.le_LEQ_IC=parent.le_LEQ_IC
        
        self.le_Sxeq_EC=parent.le_Sxeq_EC
        self.le_Syeq_EC=parent.le_Syeq_EC
        self.le_Sxir_EC=parent.le_Sxir_EC
        self.le_Syir_EC=parent.le_Syir_EC
        self.le_ER_EC=parent.le_ER_EC
        self.le_IR_EC=parent.le_IR_EC
        self.le_SL_EC=parent.le_SL_EC
        self.le_LEQ_EC=parent.le_LEQ_EC
        
        self.dataI=[]
        self.dataI.append(self.le_Sxeq_IC.text())
        self.dataI.append(self.le_Syeq_IC.text())
        self.dataI.append(self.le_Sxir_IC.text())
        self.dataI.append(self.le_Syir_IC.text())
        self.dataI.append(self.le_ER_IC.text())
        self.dataI.append(self.le_IR_IC.text())
        self.dataI.append(self.le_SL_IC.text())
        self.dataI.append(self.le_LEQ_IC.text())
        
        self.TW.setStyleSheet("""
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

        self.innerCell=False
        for i in range(len(self.dataI)):
            if self.dataI[i]=='':
                self.innerCell=False
                break
            self.innerCell=True

        while (self.TW.rowCount() > 0):
            self.TW.removeRow(0)
        
        # path=os.getcwd()+'\\CellDb.txt'
        # if os.path.exists(path):
        #     file=open(path,'r')
        # else:
        #     file=open(path,'w')
        #     file.close()
        #     file=open(path,'r')
        # linee=file.readlines()
        # file.close()
        # rowPosition = self.TW.rowCount()
        
        # if self.innerCell:
        #     diameter=self.dataI[4]

        #     for i in range(len(linee)):
        #         line=linee[i].split(';')
        #         self.TW.insertRow(rowPosition)
        #         if float(line[5])==float(diameter):
        #             self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[0])))
        #             self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[1])))
        #             self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[2])))
        #             self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[3])))
        #             self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[4])))
        #             self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[5])))
        #             self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[6])))
        #             self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[7])))
        #             self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[8])))
        #             self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[9])))
        #             self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[10])))
        #             self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[11])))
        #             self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[12])))
        #             self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[13])))
        #             self.TW.setItem(rowPosition , 0, QTableWidgetItem(str(line[14])))            
    
        # else:
            
        #     for i in range(len(linee)):
        #         line=linee[i].split(';')
        #         self.TW.insertRow(rowPosition)
        #         self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[0])))
        #         self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[1])))
        #         self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[2])))
        #         self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[3])))
        #         self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[4])))
        #         self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[5])))
        #         self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[6])))
        #         self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[7])))
        #         self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[8])))
        #         self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[9])))
        #         self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[10])))
        #         self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[11])))
        #         self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[12])))
        #         self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[13])))
        #         self.TW.setItem(rowPosition , 0, QTableWidgetItem(str(line[14])))
                
        # self.TW.cellClicked.connect(self.tablewidget_clicked)

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
        
##############################################################################
        
    def tablewidget_clicked(self):
        if QtCore.Qt.LeftButton:
            current_row = self.TW.currentRow()
        
##############################################################################

    def button_cancel(self):
        self.close()   

##############################################################################

    def button_import_automatic(self):
        try:
            try:
                self.pathDB = self.path_to_elmg_file+'\\DB_file'
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
                
                rowPosition = self.TW.rowCount()
                for i in range(len(read)):
                    line=read[i].split(';')
                    if self.innerCell:
                        diameter=self.dataI[4]
                        #if str(line[0]).__contains__('HC') and float(line[7])==float(diameter):
                        if str(line[0]).__contains__('HC'):                         
                            self.TW.insertRow(rowPosition)
                            self.TW.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                            self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                            self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                            self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                            self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                            self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                            self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                            self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                            self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                            self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                            self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                            self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                            self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                            self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                            self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                            self.TW.setItem(rowPosition , 15, QTableWidgetItem(str(line[16])))
                            cell_item=self.TW.item(rowPosition, 1)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 2)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 3)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 4)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 5)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 6)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 7)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 8)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 9)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 10)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 11)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 12)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 13)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 14)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 15)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    else:
                        if str(line[0]).__contains__('HC'):
                            self.TW.insertRow(rowPosition)
                            self.TW.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                            self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                            self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                            self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                            self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                            self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                            self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                            self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                            self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                            self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                            self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                            self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                            self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                            self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                            self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                            self.TW.setItem(rowPosition , 15, QTableWidgetItem(str(line[16])))
                            cell_item=self.TW.item(rowPosition, 1)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 2)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 3)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 4)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 5)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 6)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 7)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 8)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 9)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 10)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 11)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 12)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 13)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 14)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 15)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
            self.TW.cellClicked.connect(self.tablewidget_clicked)
        except:
            self.warning_wdj('Import failed. Retry')

##############################################################################

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
                
                rowPosition = self.TW.rowCount()
                for i in range(len(read)):
                    line=read[i].split(';')
                    if self.innerCell:
                        diameter=self.dataI[4]
                        # comment --> regola: diametro eq IC = diametro eq EC
                        # ho tolto la regola per permettere di sistemare il diametro dopo (in modo da non dover
                        # avere i diametri identici (dopo tuning)))
                        #if str(line[0]).__contains__('HC') and float(line[7])==float(diameter):
                        if str(line[0]).__contains__('HC'):
                            self.TW.insertRow(rowPosition)
                            self.TW.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                            self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                            self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                            self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                            self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                            self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                            self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                            self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                            self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                            self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                            self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                            self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                            self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                            self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                            self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                            self.TW.setItem(rowPosition , 15, QTableWidgetItem(str(line[16])))
                            cell_item=self.TW.item(rowPosition, 1)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 2)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 3)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 4)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 5)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 6)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 7)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 8)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 9)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 10)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 11)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 12)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 13)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 14)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 15)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    else:
                        if str(line[0]).__contains__('HC'):
                            self.TW.insertRow(rowPosition)
                            self.TW.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                            self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                            self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                            self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                            self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                            self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                            self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                            self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                            self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                            self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                            self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                            self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                            self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                            self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                            self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                            self.TW.setItem(rowPosition , 15, QTableWidgetItem(str(line[16])))
                            cell_item=self.TW.item(rowPosition, 1)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 2)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 3)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 4)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 5)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 6)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 7)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 8)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 9)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 10)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 11)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 12)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 13)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 14)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            cell_item=self.TW.item(rowPosition, 15)
                            cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
            self.TW.cellClicked.connect(self.tablewidget_clicked)
        except:
            self.warning_wdj('Import failed. Retry')
            
##############################################################################

    def button_ok(self):
        row1=[]
        cont=0
        for currentQTableWidgetItem in self.TW.selectedItems():
            cont+=1
            row1.append(currentQTableWidgetItem.text())
            
        if cont == 1:
            row1=[]
            freq=0
            
            try:
                current_row = self.TW.currentRow()
                for i in range(1,11):
                    if i!=1:
                        row1.append(self.TW.item(current_row, i).text())
                    else:
                        freq=self.TW.item(current_row, i).text()
            except:
                self.warning_wdj('no row selected')
        
        if cont>0:
            self.le_f.setText(freq)
            self.le_Sxeq_EC.setText(row1[0])
            self.le_Syeq_EC.setText(row1[1])
            self.le_Sxir_EC.setText(row1[2])
            self.le_Syir_EC.setText(row1[3])
            self.le_ER_EC.setText(row1[4])
            self.le_IR_EC.setText(row1[5])
            self.le_SL_EC.setText(row1[6])
            self.le_LEQ_EC.setText(row1[8])
        self.close()
        return(row1)
    
##############################################################################
        
    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass   