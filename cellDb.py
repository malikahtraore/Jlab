# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 14:05:29 2022

@author: edelcore
"""

from PyQt5 import uic, QtCore
import PyQt5.QtCore as Qt
from PyQt5.QtWidgets import QWidget, QDialog, QFileDialog, QMessageBox
import os
from PyQt5.QtGui import QPixmap, QIcon
from os.path import normpath, isdir
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

EGui, QtBaseClass = uic.loadUiType('SingleCell.ui')

class CellDb(QDialog, EGui):    
    def __init__(self, parent, row1, row2):
        super(CellDb, self).__init__(parent)
        QWidget.__init__(self)
        EGui.__init__(self)
        self.setupUi(self)
                
        self.row1=row1
        self.row2=row2
        self.nameList=[]
        self.pathDB=''
        
        self.path_to_elmg_file=parent.path_to_elmg_file

        self.le_Sxeq_IC_2=parent.le_Sxeq_IC_2
        self.le_Syeq_IC_2=parent.le_Syeq_IC_2
        self.le_Sxir_IC_2=parent.le_Sxir_IC_2
        self.le_Syir_IC_2=parent.le_Syir_IC_2
        self.le_ER_IC_2=parent.le_ER_IC_2
        self.le_IR_IC_2=parent.le_IR_IC_2
        self.le_SL_IC_2=parent.le_SL_IC_2
        self.le_Sxeq_EC_2=parent.le_Sxeq_EC_2
        self.le_Syeq_EC_2=parent.le_Syeq_EC_2
        self.le_Sxir_EC_2=parent.le_Sxir_EC_2
        self.le_Syir_EC_2=parent.le_Syir_EC_2
        self.le_ER_EC_2=parent.le_ER_EC_2
        self.le_IR_EC_2=parent.le_IR_EC_2
        self.le_SL_EC_2=parent.le_SL_EC_2
        self.SF_param=parent.SF_param

        self.le_f_3=parent.le_f_3
        self.le_beta_3=parent.le_beta_3
        self.le_tube_length_2=parent.le_tube_length_2
        self.le_tube_length_Rir_2=parent.le_tube_length_Rir_2
        self.lb_se_f_2=parent.lb_se_f_2
        
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        
        self.tempArray=parent.tempArray
        self.pb_Add.setEnabled(False)
        self.SF_param0=self.tempArray[0,0]
        self.qbcs=self.tempArray[0,1]
        self.rq=self.tempArray[0,2]
        self.EpEacc=self.tempArray[0,3]
        self.HpEacc=self.tempArray[0,4]
        self.K=self.tempArray[0,5]
        
        
        self.row=''
        for i in range(len(self.row1)):
            self.row += (self.row1[i]).replace('\n','')+';'
        for i in range(len(self.row2)):
            if i==len(self.row2)-1:
                self.row+=self.row2[i]+'\n'
            else:
                self.row+=self.row2[i].replace('\n','')+';'
                
        self.param_DB=parent.param_DB
        self.pb_OK.clicked.connect(self.button_ok)
        self.pb_cancel.clicked.connect(self.button_cancel)
        self.pb_Add.clicked.connect(self.add_to_db)
        
        self.pushButton_GetEG.clicked.connect(self.getEG)
        self.pushButton_Import.clicked.connect(self.Import)
        self.pushButton_Delete.clicked.connect(self.Delete)
        self.pushButton_View.clicked.connect(self.View)
        if self.lb_se_f_2.text().__contains__('0') or self.lb_se_f_2.text().__contains__('1') or self.lb_se_f_2.text().__contains__('2') or self.lb_se_f_2.text().__contains__('3') or self.lb_se_f_2.text().__contains__('4') or self.lb_se_f_2.text().__contains__('5') or self.lb_se_f_2.text().__contains__('6') or self.lb_se_f_2.text().__contains__('7') or self.lb_se_f_2.text().__contains__('8') or self.lb_se_f_2.text().__contains__('9') or self.lb_se_f_2.text().__contains__('10'):
            self.pushButton_GetEG.setEnabled(True)
        else:
            self.pushButton_GetEG.setEnabled(False)

        try:
            self.Import_automatic()
        except:
            self.warning_wdj('Errors opening the DB')
        
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

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        
##############################################################################

    def button_cancel(self):
        self.close() 
        return self.pathDB

##############################################################################
           
    def Import_automatic(self):
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
                
                while (self.TW.rowCount() > 0):
                    self.TW.removeRow(0)
                
                rowPosition = self.TW.rowCount()
                for i in range(len(read)):
                    line=read[i].split(';')
                    if str(line[0]).__contains__('SC'):
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
                        self.TW.setItem(rowPosition , 16, QTableWidgetItem(str(line[17])))
                        self.TW.setItem(rowPosition , 17, QTableWidgetItem(str(line[18])))
                        self.TW.setItem(rowPosition , 18, QTableWidgetItem(str(line[19])))
                        self.TW.setItem(rowPosition , 19, QTableWidgetItem(str(line[20])))
                        self.TW.setItem(rowPosition , 20, QTableWidgetItem(str(line[21])))
                        self.TW.setItem(rowPosition , 21, QTableWidgetItem(str(line[22])))
                        self.TW.setItem(rowPosition , 22, QTableWidgetItem(str(line[23])))
                        self.TW.setItem(rowPosition , 23, QTableWidgetItem(str(line[24])))
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
                        cell_item=self.TW.item(rowPosition, 16)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 17)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 18)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 19)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 20)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 21)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 22)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 23)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    self.pb_Add.setEnabled(True)
        except:
            self.warning_wdj('Import failed. Retry')
        
        return self.pathDB
    
##############################################################################

    def button_ok(self):
        try:
            numberRows=self.TW.rowCount()
            a=[]
            
            #### read HC and save
            file=open(self.pathDB,'r')
            linee=file.readlines()
            file.close()
            hc=[]
            for i in range(len(linee)):
                if linee[i].startswith('HC') or linee[i].startswith('EG'):
                    hc.append(linee[i])
            
            for row in range(numberRows):
                a.append('SC;')
                for col in range(24):
                    if col!=23:
                        a.append(self.TW.item(row, col).text()+';')
                    else:
                        a.append(self.TW.item(row, col).text())
                if row!=numberRows-1:
                    a.append('\n')
                elif row==numberRows-1 and len(hc)!=0:
                    a.append('\n')
            try:
                filedb=open(self.pathDB,'w')
                for i in range(len(a)):
                    filedb.writelines(a[i])
                for i in range(len(hc)):
                    filedb.writelines(hc[i])
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
                    if lineeDB[i].startswith('EG') or lineeDB[i].startswith('HC') or lineeDB[i].startswith('SC'):
                        l.append(lineeDB[i])
                fileDB=open(self.pathDB,'w')
                lineeDB=fileDB.writelines(l)
                fileDB.close()
            except:
                self.warning_wdj('Some errors writing the db file')    
            
            return self.pathDB
        except:
            self.close()
            

        
##############################################################################

    def add_to_db(self):
        try:
            if self.pathDB!='' and self.textEdit_EndGroup.toPlainText()!='':
                if os.path.exists(self.pathDB):
                    file=open(self.pathDB,'r')
                    linee=file.readlines()
                    file.close()
                    file=open(self.pathDB,'w')
                    for i in range(len(linee)):
                        if i==len(linee)-1:
                            file.writelines(linee[i]+'\n')
                        else:
                            file.writelines(linee[i])
        
                    if len(self.row.split(';'))==25:
                        file.writelines(self.row)
                    file.close()
                
                else:
                    file=open(self.pathDB,'w')
                    file.writelines(self.row)
                    file.close()
                  
                rowPosition = self.TW.rowCount()
                #### end group name
                try:
                    if self.textEdit_EndGroup.toPlainText()!='':
                        cont=0
                        
                        # self.nameList
                        self.nameList=[]
                        for i in range(self.TW.rowCount()):
                            self.nameList.append(self.TW.item(i, 0).text())

                        for i in range(len(self.nameList)):
                            if self.nameList[i]==self.textEdit_EndGroup.toPlainText():
                                self.warning_wdj('Another cell has the same name. Please insert a new name.')
                                break
                            else:
                                cont+=1

                        if cont==len(self.nameList):
                            endGroupName=self.textEdit_EndGroup.toPlainText()
                            try:
                                line=[]
                                line.append(endGroupName+';')
                                #line.append(str(self.SF_param0)+';')
                                line.append(self.le_f_3.text()+';')
                                line.append(self.le_beta_3.text().replace('\n','').replace(',','')+';')
                                line.append(str(round(float(self.SF_param[5])/10,2))+';')
                                #line.append(self.lb_se_E.text()+';')
                                line.append(str(round(float(self.SF_param[6]) * 0.0012566370614359172/10,2))+';')
                                #line.append(self.lb_se_H.text()+';')
                                line.append(str(self.SF_param[3])+';')
                                #line.append(self.lb_se_q.text()+';')
                                line.append(str(self.SF_param[2])+';')
                                #line.append(self.lb_se_rq.text()+';')
                                line.append(str(self.SF_param[7])+';')
                                #line.append(self.lb_se_K.text()+';')
                                line.append(self.le_Sxeq_IC_2.text()+';')
                                line.append(self.le_Syeq_IC_2.text()+';')
                                line.append(self.le_Sxir_IC_2.text()+';')
                                line.append(self.le_Syir_IC_2.text()+';')
                                line.append(self.le_ER_IC_2.text()+';')
                                line.append(self.le_IR_IC_2.text()+';')
                                line.append(self.le_SL_IC_2.text()+';')
                                line.append(self.le_Sxeq_EC_2.text()+';')
                                line.append(self.le_Syeq_EC_2.text()+';')
                                line.append(self.le_Sxir_EC_2.text()+';')
                                line.append(self.le_Syir_EC_2.text()+';')
                                line.append(self.le_ER_EC_2.text()+';')
                                line.append(self.le_IR_EC_2.text()+';')
                                line.append(self.le_SL_EC_2.text()+';')
                                line.append(self.le_tube_length_2.text()+';')
                                line.append(self.le_tube_length_Rir_2.text()+';')
                                
                                self.TW.insertRow(rowPosition)
                                self.TW.setItem(rowPosition , 0, QTableWidgetItem(endGroupName.replace(';','')))
                                self.TW.setItem(rowPosition , 1, QTableWidgetItem(str(line[1]).replace(';','')))
                                self.TW.setItem(rowPosition , 2, QTableWidgetItem(str(line[2]).replace(';','')))
                                self.TW.setItem(rowPosition , 3, QTableWidgetItem(str(line[3]).replace(';','')))
                                self.TW.setItem(rowPosition , 4, QTableWidgetItem(str(line[4]).replace(';','')))
                                self.TW.setItem(rowPosition , 5, QTableWidgetItem(str(line[5]).replace(';','')))
                                self.TW.setItem(rowPosition , 6, QTableWidgetItem(str(line[6]).replace(';','')))
                                self.TW.setItem(rowPosition , 7, QTableWidgetItem(str(line[7]).replace(';','')))
                                self.TW.setItem(rowPosition , 8, QTableWidgetItem(str(line[8]).replace(';','')))
                                self.TW.setItem(rowPosition , 9, QTableWidgetItem(str(line[9]).replace(';','')))
                                self.TW.setItem(rowPosition , 10, QTableWidgetItem(str(line[10]).replace(';','')))
                                self.TW.setItem(rowPosition , 11, QTableWidgetItem(str(line[11]).replace(';','')))
                                self.TW.setItem(rowPosition , 12, QTableWidgetItem(str(line[12]).replace(';','')))
                                self.TW.setItem(rowPosition , 13, QTableWidgetItem(str(line[13]).replace(';','')))
                                self.TW.setItem(rowPosition , 14, QTableWidgetItem(str(line[14]).replace(';','')))
                                self.TW.setItem(rowPosition , 15, QTableWidgetItem(str(line[15]).replace(';','')))
                                self.TW.setItem(rowPosition , 16, QTableWidgetItem(str(line[16]).replace(';','')))
                                self.TW.setItem(rowPosition , 17, QTableWidgetItem(str(line[17]).replace(';','')))
                                self.TW.setItem(rowPosition , 18, QTableWidgetItem(str(line[18]).replace(';','')))
                                self.TW.setItem(rowPosition , 19, QTableWidgetItem(str(line[19]).replace(';','')))
                                self.TW.setItem(rowPosition , 20, QTableWidgetItem(str(line[20]).replace(';','')))
                                self.TW.setItem(rowPosition , 21, QTableWidgetItem(str(line[21]).replace(';','')))
                                self.TW.setItem(rowPosition , 22, QTableWidgetItem(str(line[22]).replace(';','')))
                                self.TW.setItem(rowPosition , 23, QTableWidgetItem(str(line[23]).replace(';','')))
                    
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
                                cell_item=self.TW.item(rowPosition, 16)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 17)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 18)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 19)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 20)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 21)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 22)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                cell_item=self.TW.item(rowPosition, 23)
                                cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                            except:
                                self.warning_wdj('Errors in EndGroup DB add')                        
                except:
                    self.warning_wdj('Errors in EndGroup DB')
            elif self.textEdit_EndGroup.toPlainText()=='':
                self.warning_wdj('Please insert a valid EndGroup name')
            else:
                self.warning_wdj('Please import a db file or save a new one')
        except:
            self.warning_wdj('Errors in EndGroup DB')
            
##############################################################################
        
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

    def getEG(self):
        try:
            if self.textEdit_EndGroup.toPlainText() != '':
                endGroupName=self.textEdit_EndGroup.toPlainText()
                
                try:
                    self.pathDB, _ = QFileDialog.getSaveFileName(self,"Save DB", "\\home", "*.txt")
                    
                    self.pathDB = normpath(str(self.pathDB))
                    ok = 1
                except:
                    ok=0
                
                if ok == 1:
                    filedb=open(self.pathDB, 'w')
                    numberRows=self.TW.rowCount()
                    a=[]
                    for row in range(numberRows):
                        a.append('EG')
                        for col in range(25):
                            if col==24:
                                a.append(self.TW.item(row, col).text()+'\n')
                            else:
                                a.append(self.TW.item(row, col).text()+';')
                    filedb.writelines(a)
                    filedb.close() 
                    self.pb_Add.setEnabled(True)
            else:
                self.warning_wdj('Please insert a valid endGroup name')
                
        except:
            self.warning_wdj('Saving Failed. Retry')
 
##############################################################################
           
    def Import(self):
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
                
                while (self.TW.rowCount() > 0):
                    self.TW.removeRow(0)
                
                rowPosition = self.TW.rowCount()
                for i in range(len(read)):
                    line=read[i].split(';')
                    if str(line[0]).__contains__('SC'):
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
                        self.TW.setItem(rowPosition , 16, QTableWidgetItem(str(line[17])))
                        self.TW.setItem(rowPosition , 17, QTableWidgetItem(str(line[18])))
                        self.TW.setItem(rowPosition , 18, QTableWidgetItem(str(line[19])))
                        self.TW.setItem(rowPosition , 19, QTableWidgetItem(str(line[20])))
                        self.TW.setItem(rowPosition , 20, QTableWidgetItem(str(line[21])))
                        self.TW.setItem(rowPosition , 21, QTableWidgetItem(str(line[22])))
                        self.TW.setItem(rowPosition , 22, QTableWidgetItem(str(line[23])))
                        self.TW.setItem(rowPosition , 23, QTableWidgetItem(str(line[24])))
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
                        cell_item=self.TW.item(rowPosition, 16)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 17)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 18)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 19)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 20)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 21)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 22)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                        cell_item=self.TW.item(rowPosition, 23)
                        cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    self.pb_Add.setEnabled(True)
        except:
            self.warning_wdj('Import failed. Retry')
        
        return self.pathDB
                
##############################################################################        
        
    def Delete(self):
        reply=self.delete_wdj('Are you sure you want to delete the row?')
        if reply == QMessageBox.Yes:
            if QtCore.Qt.LeftButton:
                current_row = self.TW.currentRow()
                self.TW.removeRow(current_row)
        else:
            pass

##############################################################################        
        
    def View(self):
        try:
            cont=0
            if QtCore.Qt.LeftButton:
                current_row = self.TW.currentRow()
                cont+=1
                
            if cont==1:
                row1=[]
                try:
                    current_row = self.TW.currentRow()
                    for i in range(24):
                        row1.append(self.TW.item(current_row, i).text())
                except:
                    self.warning_wdj('no row selected')
                
            if cont>0:
                self.le_f_3.setText(row1[1])
                self.le_beta_3.setText(row1[2])
                self.le_tube_length_2.setText(row1[22])
                self.le_tube_length_Rir_2.setText(row1[23])
                self.le_Sxeq_IC_2.setText(row1[8])
                self.le_Syeq_IC_2.setText(row1[9])
                self.le_Sxir_IC_2.setText(row1[10])
                self.le_Syir_IC_2.setText(row1[11])
                self.le_ER_IC_2.setText(row1[12])
                self.le_IR_IC_2.setText(row1[13])
                self.le_SL_IC_2.setText(row1[14])
                self.le_Sxeq_EC_2.setText(row1[15])
                self.le_Syeq_EC_2.setText(row1[16])
                self.le_Sxir_EC_2.setText(row1[17])
                self.le_Syir_EC_2.setText(row1[18])
                self.le_ER_EC_2.setText(row1[19])
                self.le_IR_EC_2.setText(row1[20])
                self.le_SL_EC_2.setText(row1[21])
            self.close()
            return(row1)
        except:
            self.warning_wdj('Something goes wrong. Retry')