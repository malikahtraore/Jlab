# -*- coding: utf-8 -*-
"""
Created on Mon May 23 15:29:00 2022

@author: edelcore

Fill the HC and EG tables from database and choose how to build the multicell
Run the electromagnetic simulation for multicell cavity
Define field data plot , useful for cavity output window
"""

from PyQt5.QtWidgets import QWidget, QDialog, QFileDialog, QVBoxLayout, QLabel, QSizePolicy
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from Press_Button_ELMG_simulation import Press_Button_ELMG_simulation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.pyplot import figure as plt_figure
from cavityOutput import cavityOutput
from subprocess import call as scall
from os import remove, rename
from os.path import isdir, normpath

multicellui, QtBaseClass = uic.loadUiType('multicell.ui')

class multicell(QDialog, multicellui):
    def __init__(self, parent, CAV, pathDB):
        super(multicell, self).__init__(parent)
        QWidget.__init__(self)
        multicellui.__init__(self)
        self.setupUi(self)
        
        self.CAV = np.zeros((5,8))
        #self.CAV = CAV
        self.elmg_param = np.zeros((1,25))
        self.pathDB=pathDB
        self.path_to_elmg_file=parent.path_to_elmg_file
        self.output_file=parent.path_to_elmg_file+'\\outp_file'

        self.elmg_param[0,0]=10
        self.elmg_param[0,2]=2
        self.elmg_param[0,3]=1
        self.elmg_param[0,4]=1
        self.elmg_param[0,22]=-2
        self.i=0
        self.peaks=[]
        
        self.nameIC=''
        self.nameEG1=''
        self.nameEG2=''
        self.p=np.zeros((3,5))
        
        self.label2 = QLabel(self)
        self.pixmap2 = QPixmap()
        self.figure_3 = plt_figure(figsize=(10, 8), dpi=100)    
        self.canvas_3 = FigureCanvas(self.figure_3)   
        self.canvas_3.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas_3, self)
        self.lay_plot.addWidget(self.toolbar)
        self.lay_plot.addWidget(self.canvas_3)
        
        self.textEdit_NumberCell.setInputMask("00")
        
        try:
                    
            pathDB=self.pathDB
            
            MW_path = os.getcwd()
            self.button_init()
            self.pushButton_SuperfishExecution.clicked.connect(self.Superfish_execution)
            
            self.pushButton_Quit.clicked.connect(self.click_Quit)
            self.path = parent.path_to_elmg_file
            
            self.arrayIC=[]
            self.arrayEG=[]
            
            #### Database Inner Cell
            path_fileI=pathDB
            if os.path.exists(path_fileI):
                fileI=open(path_fileI,'r')
            else:
                fileI=open(path_fileI,'w')
                fileI.close()
                fileI=open(path_fileI,'r')
            linee=fileI.readlines()
            fileI.close()
            rowPosition = self.tableWidget.rowCount()
            
            for i in range(len(linee)):
                line=linee[i].split(';')
                if line[0]=='HC':
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
                    self.arrayIC.append(str(line[1]))
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
                
            #### Database End Group
            path_fileEG=pathDB
            if os.path.exists(path_fileEG):
                fileEG=open(path_fileEG,'r')
            else:
                fileEG=open(path_fileEG,'w')
                fileEG.close()
                fileEG=open(path_fileEG,'r')
            lineeEG=fileEG.readlines()
            fileEG.close()
            rowPosition = self.tableWidget_3.rowCount()
            
            for i in range(len(lineeEG)):
                line=lineeEG[i].split(';')
                if line[0]=='EG':
                    self.tableWidget_3.insertRow(rowPosition)
                    self.tableWidget_3.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                    self.tableWidget_3.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                    self.tableWidget_3.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                    self.tableWidget_3.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                    self.tableWidget_3.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                    self.tableWidget_3.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                    self.tableWidget_3.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                    self.tableWidget_3.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                    self.tableWidget_3.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                    self.tableWidget_3.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                    self.tableWidget_3.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                    self.tableWidget_3.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                    self.tableWidget_3.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                    self.tableWidget_3.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                    self.tableWidget_3.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                    self.tableWidget_3.setItem(rowPosition , 15, QTableWidgetItem(str(line[16])))
                    self.tableWidget_3.setItem(rowPosition , 16, QTableWidgetItem(str(line[17])))
                    self.tableWidget_3.setItem(rowPosition , 17, QTableWidgetItem(str(line[18])))
                    self.tableWidget_3.setItem(rowPosition , 18, QTableWidgetItem(str(line[19])))
                    self.tableWidget_3.setItem(rowPosition , 19, QTableWidgetItem(str(line[20])))
                    self.tableWidget_3.setItem(rowPosition , 20, QTableWidgetItem(str(line[21])))
                    self.tableWidget_3.setItem(rowPosition , 21, QTableWidgetItem(str(line[22])))
                    self.tableWidget_3.setItem(rowPosition , 22, QTableWidgetItem(str(line[23])))
                    self.tableWidget_3.setItem(rowPosition , 23, QTableWidgetItem(str(line[24])))
                    self.arrayEG.append(str(line[1]))
                    cell_item=self.tableWidget_3.item(rowPosition, 1)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 2)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 3)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 4)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 5)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 6)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 7)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 8)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 9)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 10)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 11)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 12)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 13)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 14)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 15)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 16)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 17)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 18)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 19)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 20)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 21)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 22)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    cell_item=self.tableWidget_3.item(rowPosition, 23)
                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                    
            self.cb_InnerCell.setEditable(True)
            self.cb_InnerCell.addItems(self.arrayIC)        
            self.cb_EndGroup1.setEditable(True)
            self.cb_EndGroup1.addItems(self.arrayEG)        
            self.cb_EndGroup2.setEditable(True)
            self.cb_EndGroup2.addItems(self.arrayEG)        

        except:
            self.warning_wdj('Choose a db file to proceed')

##############################################################################
        # Logo
        
        MC_path = os.getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)
        
##############################################################################
        
    def button_init(self):
        MW_path = os.getcwd()
        
        pLayout2 = QVBoxLayout()
        pIconLabel2 = QLabel()
        pTextLabel2 = QLabel() 
                
        title_fig = QPixmap(MW_path + '\\multicell_img.png')
        title_fig_resized = title_fig.scaled(90, 70, Qt.KeepAspectRatio)
        pIconLabel2.setPixmap(title_fig_resized)
        pIconLabel2.setAlignment(Qt.AlignCenter)
        pIconLabel2.setMouseTracking(False)
        pIconLabel2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        pTextLabel2.setText("RF cav")
        pTextLabel2.setAlignment(Qt.AlignCenter)
        pTextLabel2.setWordWrap(True)
        pTextLabel2.setTextInteractionFlags(Qt.NoTextInteraction)
        pTextLabel2.setMouseTracking(False)
        pTextLabel2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        pLayout2.addWidget(pIconLabel2)
        pLayout2.addWidget(pTextLabel2)
        
        self.pushButton_SuperfishExecution.setLayout(pLayout2)
        
##############################################################################
        
    def Superfish_execution(self):
        
        self.nameIC = self.cb_InnerCell.currentText()
        self.nameEG1 = self.cb_EndGroup1.currentText()
        self.nameEG2 = self.cb_EndGroup2.currentText()
        
        # IC
        
        file1=open(self.pathDB,'r')
        line1=file1.readlines()
        file1.close()
        
        for i in range(len(line1)):
            if not line1[i].startswith('\n'):
                line=line1[i].split(';')
                if line[1]==self.nameIC and line[0]=='HC':
                    self.CAV[2,0]=line[3]
                    self.CAV[2,1]=line[4]
                    self.CAV[2,2]=line[5]
                    self.CAV[2,3]=line[6]
                    self.CAV[2,4]=line[7]
                    self.CAV[2,5]=line[8]
                    self.CAV[2,6]=line[9]
                    self.p[0,0]=line[2]
                    self.p[0,1]=line[11]
                    self.p[0,2]=line[12]
                    self.p[0,3]=line[15]
                if line[1]==self.nameEG1 and line[0]=='EG':
                    self.CAV[1,0]=line[9]
                    self.CAV[1,1]=line[10]
                    self.CAV[1,2]=line[11]
                    self.CAV[1,3]=line[12]
                    self.CAV[1,4]=line[13]
                    self.CAV[1,5]=line[14]
                    self.CAV[1,6]=line[15]
                    self.CAV[0,0]=line[16]
                    self.CAV[0,1]=line[17]
                    self.CAV[0,2]=line[18]
                    self.CAV[0,3]=line[19]
                    self.CAV[0,4]=line[20]
                    self.CAV[0,5]=line[21]
                    self.CAV[0,6]=line[22]
                    self.CAV[1,7]=line[23]
                    self.CAV[2,7]=line[24]
                    self.p[1,0]=line[2]
                    self.p[1,1]=line[4]
                    self.p[1,2]=line[5]
                    self.p[1,3]=line[23]
                    self.p[1,4]=line[24]
                if line[1]==self.nameEG2 and line[0]=='EG':
                    self.CAV[4,0]=line[9]
                    self.CAV[4,1]=line[10]
                    self.CAV[4,2]=line[11]
                    self.CAV[4,3]=line[12]
                    self.CAV[4,4]=line[13]
                    self.CAV[4,5]=line[14]
                    self.CAV[4,6]=line[15]
                    self.CAV[3,0]=line[16]
                    self.CAV[3,1]=line[17]
                    self.CAV[3,2]=line[18]
                    self.CAV[3,3]=line[19]
                    self.CAV[3,4]=line[20]
                    self.CAV[3,5]=line[21]
                    self.CAV[3,6]=line[22]
                    self.CAV[3,7]=line[23]
                    self.CAV[4,7]=line[24]
                    self.p[2,0]=line[2]
                    self.p[2,1]=line[4]
                    self.p[2,2]=line[5]
                    self.p[2,3]=line[23]
                    self.p[2,4]=line[24]
            
        #### Superfish for the multicell
        numberCell = 0
        contSuper=0
        try:
            if self.textEdit_NumberCell.text()!='':
                
                if not str(self.textEdit_NumberCell.text()).isdigit():
                    self.warning_wdj('The number of cells must be a valid integer number')
                elif not float(self.textEdit_NumberCell.text()).is_integer():
                        self.warning_wdj('The number of cells must be an integer number')
                else:
                    numberCells=int(self.textEdit_NumberCell.text().replace(' ','').replace('\t','').replace('\n','').replace('  ',''))
                    self.CAV[0,7] = numberCells
                    contSuper+=1
            else:
                self.warning_wdj('Please insert a number of cells')
                
        except:
            self.warning_wdj('Errors reading Number Cells')
        
        self.elmg_param[0,1]=self.CAV[0,4]/20

        #path="C:\\Users\\edelcore\\Desktop\\prova multicella" # da modificare
        
        path=self.path

        if contSuper==1:
             self.define_elmg_path('function')
             path=self.path
             elmg_sym=Press_Button_ELMG_simulation(self.CAV, self.path)
             elmg_sym.run_elmg_simulation()
             #new_elmg_param = elmg_sym.output_result()
             pathFile=path+'\elmg_file\log_coo_base.txt'
                          
             file=open(pathFile,'r')
             x=[]
             y=[]
             line=file.readlines()
             file.close()
             for i in range(len(line)):
                 t=re.sub('\s+',';',line[i])
                 s=t.split(';')
                 x.append(float(s[3]))
                 y.append(float(s[4]))

             fig1=plt.figure()
             plt.plot(x, y, color='red')
             plt.axis('equal')
             fig1.savefig(path+"\\figProfile.png")
             
             
             self.pixmap2 = QPixmap(path+'\\figProfile.png')
             self.label2.setPixmap(self.pixmap2)
             self.label2.setGeometry(400, 400, 581, 291)
             self.label2.setScaledContents(True)
             self.label2.move(140, 620)
             self.show()        
            
        ##############################################################################
               
             try:
                sfo_file  = open(path + '\\elmg_file\\AF_FILE.SFO', 'r')
                cont = sfo_file.readlines()
                for k in range(len(cont)-1,0,-1):
                    if str([x for x in cont[k].split(' ') if x][0]) == 'ZLONG':
                        L = float([x for x in cont[k].split(' ') if x][1])
                        break
                sfo_file.close()
                           
                af_new =  open(path + '\\elmg_file\\AF_FILE.IN7', 'w')
                cont_af = ['line	plotfiles\n', 
                          '0.0 0.0 ' + str(L) + ' 0.0\n',
                          '200\n',
                          'end']
                af_new.writelines(cont_af)
                af_new.close()
                 
                scall(path + '\\elmg_file\\AF_FILE.IN7', shell=True)
                try:
                    remove(path + '\\elmg_file\\AF_FILE_axis.TBL')
                except:
                    pass
                rename(path + '\\elmg_file\\AF_FIL01.TBL',  path + '\\elmg_file\\AF_FILE_axis.TBL')
                
                self.peaks=self.field_data(path)
                print('self.peaks ', self.peaks)
             except:
                self.critical_wdj = ('Error reading AF_FILE.SFO file.') 

        if contSuper==1:
            #Cavity output
            widget_output = cavityOutput(self, self.CAV, path, self.peaks, self.output_file)
            widget_output.exec_()
        
        
##############################################################################
        
    def click_Quit(self):
        self.close()

##############################################################################
        
    def warning_wdj(self, text):
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass 
        
###############################################################################        

    # define field data profile plot
    def field_data(self, path):      
        print('field data')  
        # Generate cavity coordinate file
        tbl_file  = open(path+'\\elmg_file\\AF_FILE_axis.TBL', 'r')
        cont = tbl_file.readlines()
        tbl_file.close()

        for k in range(0,len(cont)):
            if [x for x in cont[k].split(' ') if x][0] == 'Data\n':
                n_begin = k+3
            elif cont[k][0:7] == 'EndData':
                n_end = k
        
        fd_file  = open(path + '\\elmg_file\\field_data_axis.txt', 'w')
        fd_file.writelines(cont[n_begin : n_end])
        fd_file.close()
        
        fd_file_read=open(path+'\\elmg_file\\field_data_axis.txt', 'r')
        line=fd_file_read.readlines()
        fd_file_read.close()
        x=[]
        y=[]
        ii=[]

        for i in range(len(line)):
            t=re.sub('\s+',';',line[i])
            s=t.split(';')
            x.append(float(s[1]))
            y.append(float(s[3]))
        
        fig=plt.figure()
        plt.plot(x,y,color='red')
        plt.grid()
        plt.xlabel('Z [mm]')
        plt.ylabel('Ez [MV/m]')
        fig.savefig(path+'\\fieldProfile.png')
        
        self.peaksValues=[]
        n=self.CAV[0,7]
        # for i in range(len(z)):
        #     while n>0:
        #         self.peaksValues.append(np.max(z))
        #         z.remove(self.peaksValues[-1])
        #         n-=1
        
        for i in range(1,len(y)):
            if y[i]*y[i-1]<0:
                ii.append(i)

        for i in range(int(n)):
            if i==0:
                if y[0]<0:
                    if np.min(y[0:ii[0]])<0:
                        self.peaksValues.append(-np.min(y[0:ii[0]]))
                    else:
                        self.peaksValues.append(np.min(y[0:ii[0]]))
                else:
                    self.peaksValues.append(np.max(y[0:ii[0]]))
            elif i==n-1:
                if y[ii[-1]]<0:
                    if np.min(y[ii[-1]:len(y)])<0:
                        self.peaksValues.append(-np.min(y[ii[-1]:len(y)]))
                    else:
                        self.peaksValues.append(np.min(y[ii[-1]:len(y)]))
                else:
                    self.peaksValues.append(np.max(y[ii[-1]:len(y)]))
            else:
                if y[ii[i-1]]<0:
                    if np.min(y[ii[i-1]:ii[i]])<0:
                        self.peaksValues.append(-np.min(y[ii[i-1]:ii[i]]))
                    else:
                        self.peaksValues.append(np.min(y[ii[i-1]:ii[i]]))
                else:
                    self.peaksValues.append(np.max(y[ii[i-1]:ii[i]]))
        return self.peaksValues

 ##############################################################################
       
    def define_elmg_path(self, t):        
        if self.path == '':
            if t == 'function':
                self.warning_wdj('Select a folder where superfish file will be stored.') 
                
            while True:
                self.path = normpath(str(QFileDialog.getExistingDirectory(self, "Choose project directory",'home')))
                            
                if self.path == '.':
                    self.path = ''
                    break
                elif [y for y in [len(x.split(' ')) for x in self.path.split('\\')] if y > 1] != []:
                 self.warning_wdj('Project folder can not have space in its name.')
                else:
                    if isdir(self.path + '\\elmg_file') == False:
                        scall('mkdir '+ self.path + '\\elmg_file', shell=True)
                    break