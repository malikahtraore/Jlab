""" From line 1325 the new lines of code """
""" This is the main script of the GUI. All the functions used in the main window are defined here.
    Examples include functions connected to buttons, writing values in cells, etc.
    Anything related to modifying an element of the window is included here.
    Additionally, there are many other files that define all the underlying computations.
    """

"""From line 61 to 636: initilization of code and GUI
    """


#### import default libraries
import sys
from os import getcwd, listdir, path, remove, rename
import os
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog,  QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QTableWidgetItem
from PyQt5 import uic, QtGui, QtCore
from os.path import isdir, normpath
from subprocess import call as scall
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure as plt_figure
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from functools import partial

#### import project defined functions
from Draw_cavity_profile import Draw_cavity_profile
from Draw_cavity_profile_new import Draw_cavity_profile as Draw_cavity_profile_new # Draw_cavity_profile adapted to new parameter length
from Tune_parameters import Tune_parameters
from Mat_Prop import Mat_Prop
from db_cavity import DB
from paramDef import paramDef
from variableParam import variableParam

from endGroupDb import EndGroupDb
from info_Tube import info_Tube
from InnerCell import InnerCell
from EndCell import EndCell
from draw import draw
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # type: ignore
import re
import matplotlib.pyplot as plt # type: ignore
from Press_Button_ELMG_simulation import Press_Button_ELMG_simulation
from cavityOutput import cavityOutput
from InnerCell2 import InnerCell2 # type: ignore
from EndCell2 import EndCell2 # type: ignore
from cellDb import CellDb
import sympy as sm
from buncher_db import buncher_db


#### new functions defined in this new version
from geometry import Geometry
from electromagnetic_functions import emfn

Ui_BuildCav2, QtBaseClass = uic.loadUiType('BuildCav2_MW.ui')

class BuildCav2(QMainWindow, Ui_BuildCav2):
    def __init__(self, parent=None):
        super(BuildCav2, self).__init__(parent)
        QMainWindow.__init__(self)
        Ui_BuildCav2.__init__(self)
        self.setupUi(self)
 
############################################################################## 
        # set title and button images
               
        self.BuildCav2_version = "BuildCav2 1.0"
        self.setWindowTitle(self.BuildCav2_version)
        
        MW_path = getcwd()
        self.path_to_elmg_file = ''
        self.MATP = np.array([8.57E-6, 1.06E+5, 1.18E+5, 0.4, 0.38, 50, 1.52e-05, 0, 0.00146])
        self.round_val = 4
        self.CAV_ge = np.zeros(7)
        self.CAV_py = np.zeros(7)
        self.SF_param = [0]*9
        self.CELL = np.zeros((8))
        self.CAV=np.zeros((3,8))
        self.pathDB=''
        self.path_project=''
        
        self.frame_geometric.show()
        self.frame_phisic.hide()
        self.frame_sf_execution.hide()
        self.tune_type = 'inner'
        self.LEQ = 0 #modified by Malini
        #variable for the equator length

        self.new_parameter=0 # add by Elisa
        #self.actionClose.triggered.connect(self.Quit)
        

        self.cb_geometric.clicked.connect(partial(self.convert_pg_param, 0))
        self.cb_physic.clicked.connect(partial(self.convert_pg_param, 1))
        
        self.pb_draw_cav.clicked.connect(self.draw_cav)
        self.pb_draw_cav.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.figure = plt_figure(figsize=(10, 4), dpi=100)    
        self.canvas = FigureCanvas(self.figure)   
        self.canvas.setParent(self)
        #self.toolbar = NavigationToolbar(self.canvas, self)
        self.lay_plot.addWidget(self.canvas)
        #self.lay_plot.addWidget(self.toolbar)
        
        #self.button_init()
        #self.pb_multicell.clicked.connect(self.click_multicell)
        
        self.pb_reset_pg_param.clicked.connect(self.reset_pg_param)
        self.pb_reset_pg_param.setStyleSheet( # set button style
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_cav_database.clicked.connect(self.open_cav_database)
        self.pb_cav_database.setStyleSheet("image : url(database_img.png);") 
        self.pb_run_elmg_simulation.clicked.connect(self.button_run_elmg_simulation)
        self.pb_run_elmg_simulation.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_tune.clicked.connect(self.run_tuning)
        self.pb_tune.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_set_IC_EC.clicked.connect(self.click)
    
        self.pb_set_IC_EC.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        #self.pb_tune_EG.clicked.connect(self.set_EG_tune)
        
        self.pb_Quit.clicked.connect(self.Quit)
        self.pb_Quit.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_About.clicked.connect(self.show_about)
        self.pb_About.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        
        self.action_info.triggered.connect(self.show_info)
        self.action_about.triggered.connect(self.show_about)
        
        self.action_MATP.triggered.connect(self.set_material_properties)
        self.action_New_Project.triggered.connect(self.new_project)
        self.action_Open_Project.triggered.connect(self.open_project)
        self.action_Close_2.triggered.connect(self.Quit)
        self.actionOpen.triggered.connect(self.Open)
        
        self.frame_geometric.show()
        self.frame_phisic.hide()
        
        #### new part about tabWidget
        
        self.tabWidget.currentChanged.connect(self.change_tab)
        self.can_set_tab='no'

        self.tabWidget_2.currentChanged.connect(self.change_tab2)
        self.tabWidget_2.setStyleSheet("""
            QTabWidget::pane { /* The tab widget frame */
                border-top: 2px solid #C2C2C2;
                position: absolute;
                top: -0.5em;
            }

            QTabWidget::tab-bar {
                alignment: center;
            }

            QTabBar::tab {
                background: lightgray;
                border: 2px solid #C4C4C3;
                border-bottom-color: #C2C7CB; /* same as the pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 5px;
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                background: lightgreen;
            }
        """)
        
        self.menuFile.setStyleSheet("""
            QMenu {
                background-color: #f0f0f0;  /* Colore di sfondo del menu */
                border: 1px solid black;    /* Bordo del menu */
            }

            QMenu::item {
                background-color: transparent; /* Colore di sfondo delle voci */
                padding: 5px 25px;             /* Spaziatura interna delle voci */
            }

            QMenu::item:selected { /* Quando una voce è selezionata */
                background-color: #0078d7; /* Sfondo selezione */
                color: white;              /* Colore del testo selezionato */
            }

            QMenu::item:disabled { /* Quando una voce è disabilitata */
                color: grey; /* Colore del testo disabilitato */
            }
        """)

        self.menuHelp.setStyleSheet("""
            QMenu {
                background-color: #f0f0f0;  /* Colore di sfondo del menu */
                border: 1px solid black;    /* Bordo del menu */
            }

            QMenu::item {
                background-color: transparent; /* Colore di sfondo delle voci */
                padding: 5px 25px;             /* Spaziatura interna delle voci */
            }

            QMenu::item:selected { /* Quando una voce è selezionata */
                background-color: #0078d7; /* Sfondo selezione */
                color: white;              /* Colore del testo selezionato */
            }

            QMenu::item:disabled { /* Quando una voce è disabilitata */
                color: grey; /* Colore del testo disabilitato */
            }
        """)

        self.menuHC_var_parameters.setStyleSheet("""
            QMenu {
                background-color: #f0f0f0;  /* Colore di sfondo del menu */
                border: 1px solid black;    /* Bordo del menu */
            }

            QMenu::item {
                background-color: transparent; /* Colore di sfondo delle voci */
                padding: 5px 25px;             /* Spaziatura interna delle voci */
            }

            QMenu::item:selected { /* Quando una voce è selezionata */
                background-color: #0078d7; /* Sfondo selezione */
                color: white;              /* Colore del testo selezionato */
            }

            QMenu::item:disabled { /* Quando una voce è disabilitata */
                color: grey; /* Colore del testo disabilitato */
            }
        """)

        self.mdiArea.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

        self.mdiArea_2.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

##############################################################################
#### END GROUP FROM THIS LINE OF CODE
        #### new part about end group tab
        #self.pb_Quit_2.clicked.connect(self.Quit)
        self.pb_endGroup.clicked.connect(self.open_database)
        self.pb_endGroup.setStyleSheet("image : url(database_img.png);") 
        self.pb_interrogativo.clicked.connect(self.question)
        self.pb_interrogativo.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_reset_pg_param_2.clicked.connect(self.reset_pg_param_2)
        self.pb_reset_pg_param_2.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_choose_PC.clicked.connect(self.click_Inner)
        self.pb_choose_PC.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_choose_EC.clicked.connect(self.click_End)
        self.pb_choose_EC.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.cb_geometric_2.clicked.connect(partial(self.convert_pg_param_2, 0))
        self.cb_physic_2.clicked.connect(partial(self.convert_pg_param_2, 1))
        self.pb_run_elmg_simulation_2.clicked.connect(self.button_run_elmg_simulation_2)
        self.pb_run_elmg_simulation_2.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_tune_2.clicked.connect(self.run_tuning_2)   
        self.pb_tune_2.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        #self.pb_draw_cav_2.clicked.connect(self.draw_cav_EG)
        
        self.row1=''
        self.row2=''
        self.tempArray=np.zeros((1,6))
        self.param_DB=np.zeros((1,24))
        self.le_ER_EC.setText('')
        self.tubeLength = ''
        self.tubeL_ir = ''
        self.CAV_EG = np.zeros((2,7))
        self.CAV_ge_2 = np.zeros((3,7))
        self.CAV_py_2 = np.zeros((3,7))
        self.CAV_tuning = np.zeros((3,8))

        self.frame_phisic_2.hide()
        self.frame_sf_execution_2.hide()

        self.mdiArea_4.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

        self.mdiArea_6.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

##############################################################################
# MULTICELL FROM THIS LINE OF CODE
        self.output_file=self.path_to_elmg_file+'\\outp_file'
        
        self.nameIC=''
        self.nameEG1=''
        self.nameEG2=''
        self.p=np.zeros((3,5))
        self.elmg_param = np.zeros((1,25))
        self.peaks=[]

        self.textEdit_NumberCell_2.setInputMask("00")

        self.pushButton_SuperfishExecution.clicked.connect(self.Superfish_execution_M)
        #self.pushButton_SuperfishExecution.setStyleSheet("image : url(RFCav_SF.png);") 

        self.figure2 = plt_figure(figsize=(10, 4), dpi=100)    
        self.canvas2 = FigureCanvas(self.figure2)   
        self.canvas2.setParent(self)
        #self.toolbar = NavigationToolbar(self.canvas, self)
        self.lay_plot2.addWidget(self.canvas2)
        
        self.frame_plot.show()
        
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

        self.tableWidget_2.setStyleSheet("""
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

        self.tableWidget_4.setStyleSheet("""
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
#### Single Cell from this point
        self.pb_interrogativo_2.clicked.connect(self.question)
        self.pb_interrogativo_2.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        self.pb_reset_pg_param_3.clicked.connect(self.reset_pg_param_3)
        self.pb_reset_pg_param_3.setStyleSheet(
                                    "QPushButton::pressed"
                                    "{"
                                    "background-color : green;"
                                    "}"
                                    )
        
        self.pb_choose_PC_2.clicked.connect(self.click_Inner2) # TBD
        self.pb_choose_PC_2.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             )
        
        self.pb_choose_EC_2.clicked.connect(self.click_End2)
        self.pb_choose_EC_2.setStyleSheet(
                                        "QPushButton::pressed"
                                        "{"
                                        "background-color : green;"
                                        "}"
                                        )
        
        self.pb_run_elmg_simulation_3.clicked.connect(self.button_run_elmg_simulation_3)
        self.pb_run_elmg_simulation_3.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             ) 
        
        self.pb_tune_3.clicked.connect(self.run_tuning_2)   
        self.pb_tune_3.setStyleSheet(
                             "QPushButton::pressed"
                             "{"
                             "background-color : green;"
                             "}"
                             )

        self.pb_db_singlecell.clicked.connect(self.Database_sc)
        self.pb_db_singlecell.setStyleSheet("image : url(database_img.png);")
        
        self.cb_geometric_3.clicked.connect(partial(self.convert_pg_param_3, 0))
        self.cb_physic_3.clicked.connect(partial(self.convert_pg_param_3, 1))

        self.frame_phisic_3.hide()
        self.frame_sf_execution_3.hide()
        self.path_to_elmg_file = ''
        self.CAV = np.zeros((5,8)) # ?? non so     
        
        self.mdiArea_5.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

        self.mdiArea_7.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

##############################################################################
#### Re-entrant cavity

        self.pb_draw_cav_tab2.clicked.connect(self.draw_cav_tab2)
        self.figure_2 = plt_figure(figsize=(10, 4), dpi=100)    
        self.canvas_2 = FigureCanvas(self.figure_2)   
        self.canvas_2.setParent(self)
        self.lay_plot_2.addWidget(self.canvas_2)
    
        HH_path = getcwd()
        
        self.pb_reset_param.clicked.connect(self.reset_param_tab2)
        self.pb_go.clicked.connect(self.param_computation)

        self.pb_cav_database_2.clicked.connect(self.open_cav_database_2)
        #self.pb_cav_database_2.setStyleSheet("image : url(buncher.png);")        
        
        icon = QIcon('buncher.png')  # Sostituisci con il percorso del file immagine
        self.pb_cav_database_2.setIcon(icon)
        self.pb_cav_database_2.setIconSize(QSize(129, 180))  # Larghezza, Altezza
        
        self.mdiArea_3.setStyleSheet("""
            QMdiArea {
                background-color: #f0f0f0; /* Colore di sfondo dell'area MDI */
                border: 2px solid grey; /* Bordo dell'area MDI */
                border-radius: 10px;
            }
            QMdiSubWindow {
                border: 1px solid #0078d4; /* Bordo delle finestre MDI */
                background-color: #ffffff; /* Colore di sfondo delle finestre MDI */
            }
            QMdiSubWindow::title {
                background-color: #0078d4; /* Colore di sfondo della barra del titolo */
                color: white; /* Colore del testo nella barra del titolo */
                padding: 5px;
            }
        """)

##############################################################################
        # Logo
        
        MC_path = getcwd()
        icon = QIcon()
        icon.addPixmap(QPixmap(MC_path + '\\logo.png'), QIcon.Selected, QIcon.On)
        self.setWindowIcon(icon)

##############################################################################
    # def functions behind each tab of the main window
    
    # Outer tab: 0: cavity, 1: re-entrant cavity
    def change_tab2(self): # Outer tab
        if self.tabWidget_2.currentIndex()==0:
            self.change_tab()

    # Inner tab: 0: Half Cell, 1: End Group, 2: Multicell, 3: Single Cell
    def change_tab(self): # Inner tab
            # Half cell tab
            if self.tabWidget.currentIndex()==0:
                self.frame_halfcell.show()
                self.frame_endgroup.hide()
                self.frame_multicell.hide()
                self.frame_singlecell.hide()
                self.frame_plot.show()
                self.figure.clf()
                self.canvas.draw()
                #self.warning_wdj('Create a new project first!')

            # End Group tab
            elif self.tabWidget.currentIndex() == 1:
                self.frame_halfcell.hide()
                self.frame_endgroup.show()
                self.frame_multicell.hide()
                self.frame_singlecell.hide()
                self.frame_plot.show()
                self.set_EG_tune()
                self.figure.clf()
                self.canvas.draw()
                try:
                    if self.name_project.text()=='':
                        self.tabWidget.setCurrentIndex(0)
                        self.frame_halfcell.show()
                        self.frame_endgroup.hide()
                        self.frame_multicell.hide()
                        self.figure.clf()
                        self.canvas.draw()
                except:
                    print('Choose a db file to proceed')
                
            # Multicell tab
            elif self.tabWidget.currentIndex() == 2:
                self.frame_halfcell.hide()
                self.frame_endgroup.hide()
                self.frame_multicell.show()
                self.frame_singlecell.hide()
                self.frame_plot.hide()
                self.figure.clf()
                self.canvas.draw()        
                
                try:
                    if self.name_project.text()=='':
                        self.warning_wdj('First, you must define a new project or open an existing one')
                        self.tabWidget.setCurrentIndex(0)
                        self.frame_halfcell.show()
                        self.frame_endgroup.hide()
                        self.frame_multicell.hide()
                        self.figure.clf()
                        self.canvas.draw()
                    else:
                        ok=0       
                        self.pathDB=self.path_to_elmg_file+'\\DB_file' # retrieve db file
                        files =listdir(self.pathDB)
                        if len(files)!=0:
                            self.file_name=files[0]
                            ok=2
                        else:    
                            self.file_name='dbfile.txt'
                            file=open(self.pathDB+'\\dbfile.txt','w')
                            file.close()
                            
                        self.pathDB+='\\'+self.file_name

                        if self.pathDB=='' or ok==0:
                            self.pathDB, _ = QFileDialog.getOpenFileName(self,"Import DB", "home", "*.txt")
                            self.pathDB = normpath(str(self.pathDB))
                            try:
                                file=open(self.pathDB,'r')
                                file.close()
                            except:
                                self.warning_wdj("Choose a db ok file to proceed")
                                ok=1
                        if ok==0 or ok==2:
                            pathDB=self.pathDB

                            MW_path = getcwd()
                            self.button_init_M() # to be modified
                            
                            self.path = self.path_to_elmg_file
                            
                            self.arrayIC=[]
                            self.arrayEG=[]
                            
                            #### Database Inner Cell
                            path_fileI=pathDB
                            if path.exists(path_fileI):
                                fileI=open(path_fileI,'r')
                            else:
                                fileI=open(path_fileI,'w')
                                fileI.close()
                                fileI=open(path_fileI,'r')
                            linee=fileI.readlines()
                            fileI.close()

                            while (self.tableWidget_2.rowCount() > 0):
                                self.tableWidget_2.removeRow(0)

                            rowPosition = self.tableWidget_2.rowCount()
                            
                            for i in range(len(linee)):
                                line=linee[i].split(';')
                                if line[0]=='HC': #### fill the table with half cell values
                                    self.tableWidget_2.insertRow(rowPosition)
                                    self.tableWidget_2.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                                    self.tableWidget_2.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                                    self.tableWidget_2.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                                    self.tableWidget_2.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                                    self.tableWidget_2.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                                    self.tableWidget_2.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                                    self.tableWidget_2.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                                    self.tableWidget_2.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                                    self.tableWidget_2.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                                    self.tableWidget_2.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                                    self.tableWidget_2.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                                    self.tableWidget_2.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                                    self.tableWidget_2.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                                    self.tableWidget_2.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                                    self.tableWidget_2.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                                    self.arrayIC.append(str(line[1]))
                                    cell_item=self.tableWidget_2.item(rowPosition, 1)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 2)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 3)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 4)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 5)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 6)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 7)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 8)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 9)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 10)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 11)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 12)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 13)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_2.item(rowPosition, 14)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                
                            #### Database End Group
                            path_fileEG=pathDB
                            if path.exists(path_fileEG):
                                fileEG=open(path_fileEG,'r')
                            else:
                                fileEG=open(path_fileEG,'w')
                                fileEG.close()
                                fileEG=open(path_fileEG,'r')
                            lineeEG=fileEG.readlines()
                            fileEG.close()

                            while (self.tableWidget_4.rowCount() > 0): # clear table
                                self.tableWidget_4.removeRow(0)
                            rowPosition = self.tableWidget_4.rowCount()
                            
                            for i in range(len(lineeEG)):
                                line=lineeEG[i].split(';')
                                if line[0]=='EG': #### fill the table with the end group values
                                    self.tableWidget_4.insertRow(rowPosition)
                                    self.tableWidget_4.setItem(rowPosition , 0, QTableWidgetItem(str(line[1])))
                                    self.tableWidget_4.setItem(rowPosition , 1, QTableWidgetItem(str(line[2])))
                                    self.tableWidget_4.setItem(rowPosition , 2, QTableWidgetItem(str(line[3])))
                                    self.tableWidget_4.setItem(rowPosition , 3, QTableWidgetItem(str(line[4])))
                                    self.tableWidget_4.setItem(rowPosition , 4, QTableWidgetItem(str(line[5])))
                                    self.tableWidget_4.setItem(rowPosition , 5, QTableWidgetItem(str(line[6])))
                                    self.tableWidget_4.setItem(rowPosition , 6, QTableWidgetItem(str(line[7])))
                                    self.tableWidget_4.setItem(rowPosition , 7, QTableWidgetItem(str(line[8])))
                                    self.tableWidget_4.setItem(rowPosition , 8, QTableWidgetItem(str(line[9])))
                                    self.tableWidget_4.setItem(rowPosition , 9, QTableWidgetItem(str(line[10])))
                                    self.tableWidget_4.setItem(rowPosition , 10, QTableWidgetItem(str(line[11])))
                                    self.tableWidget_4.setItem(rowPosition , 11, QTableWidgetItem(str(line[12])))
                                    self.tableWidget_4.setItem(rowPosition , 12, QTableWidgetItem(str(line[13])))
                                    self.tableWidget_4.setItem(rowPosition , 13, QTableWidgetItem(str(line[14])))
                                    self.tableWidget_4.setItem(rowPosition , 14, QTableWidgetItem(str(line[15])))
                                    self.tableWidget_4.setItem(rowPosition , 15, QTableWidgetItem(str(line[16])))
                                    self.tableWidget_4.setItem(rowPosition , 16, QTableWidgetItem(str(line[17])))
                                    self.tableWidget_4.setItem(rowPosition , 17, QTableWidgetItem(str(line[18])))
                                    self.tableWidget_4.setItem(rowPosition , 18, QTableWidgetItem(str(line[19])))
                                    self.tableWidget_4.setItem(rowPosition , 19, QTableWidgetItem(str(line[20])))
                                    self.tableWidget_4.setItem(rowPosition , 20, QTableWidgetItem(str(line[21])))
                                    self.tableWidget_4.setItem(rowPosition , 21, QTableWidgetItem(str(line[22])))
                                    self.tableWidget_4.setItem(rowPosition , 22, QTableWidgetItem(str(line[23])))
                                    self.tableWidget_4.setItem(rowPosition , 23, QTableWidgetItem(str(line[24])))
                                    self.arrayEG.append(str(line[1]))
                                    cell_item=self.tableWidget_4.item(rowPosition, 1)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 2)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 3)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 4)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 5)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 6)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 7)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 8)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 9)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 10)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 11)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 12)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 13)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 14)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 15)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 16)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 17)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 18)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 19)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 20)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 21)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 22)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                                    cell_item=self.tableWidget_4.item(rowPosition, 23)
                                    cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)

                            self.cb_InnerCell.clear() # clear combobox
                            self.cb_InnerCell.setEditable(True)
                            self.cb_InnerCell.addItems(self.arrayIC)
                            self.cb_EndGroup1.clear()       
                            self.cb_EndGroup1.setEditable(True)
                            self.cb_EndGroup1.addItems(self.arrayEG)     
                            self.cb_EndGroup2.clear()   
                            self.cb_EndGroup2.setEditable(True)
                            self.cb_EndGroup2.addItems(self.arrayEG)        
        
                except:
                    self.warning_wdj('Choose a db file to proceed')
            
            # Single cell tab
            elif self.tabWidget.currentIndex() == 3:
                self.frame_halfcell.hide()
                self.frame_endgroup.hide()
                self.frame_multicell.hide()
                self.frame_singlecell.show()
                self.frame_plot.show()
                self.figure.clf()
                self.canvas.draw()
                try:
                    if self.name_project.text()=='':
                        self.warning_wdj('First, you must define a new project or open an existing one')
                        self.tabWidget.setCurrentIndex(0)
                        self.frame_halfcell.show()
                        self.frame_endgroup.hide()
                        self.frame_multicell.hide()
                        self.figure.clf()
                        self.canvas.draw()
                    else:
                        ok=0       
                        self.pathDB=self.path_to_elmg_file+'\\DB_file' # retrieve db file
                        files =listdir(self.pathDB)
                        if len(files)!=0:
                            self.file_name=files[0]
                            ok=2
                        else:    
                            self.file_name='dbfile.txt'
                            file=open(self.pathDB+'\\dbfile.txt','w')
                            file.close()
                            
                        self.pathDB+='\\'+self.file_name

                        if self.pathDB=='' or ok==0:
                            self.pathDB, _ = QFileDialog.getOpenFileName(self,"Import DB", "home", "*.txt")
                            self.pathDB = normpath(str(self.pathDB))
                            try:
                                file=open(self.pathDB,'r')
                                file.close()
                            except:
                                self.warning_wdj("Choose a db ok file to proceed")
                                ok=1
                        if ok==0 or ok==2:
                            pathDB=self.pathDB

                            MW_path = getcwd()
                            self.button_init_M() # to be modified
                            
                            self.path = self.path_to_elmg_file
                            
                            self.arrayIC=[]
                            self.arrayEG=[]
                            
                            #### Database Left Cell
                            path_fileI=pathDB
                            if path.exists(path_fileI):
                                fileI=open(path_fileI,'r')
                            else:
                                fileI=open(path_fileI,'w')
                                fileI.close()
                                fileI=open(path_fileI,'r')
                            linee=fileI.readlines()
                            fileI.close()

                except:
                    print('Choose a db file to proceed')
                    
##############################################################################
        
    def button_init(self):
        MW_path = getcwd()
        pLayout = QHBoxLayout()
        pIconLabel = QLabel()
        pTextLabel = QLabel() 
                
        title_fig = QPixmap(MW_path + '\\database_img.png')
        title_fig_resized = title_fig.scaled(90, 52, Qt.KeepAspectRatio)
        pIconLabel.setPixmap(title_fig_resized)
        pIconLabel.setAlignment(Qt.AlignCenter)
        pIconLabel.setMouseTracking(False)
        pIconLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        pTextLabel.setText("Database")
        pTextLabel.setAlignment(Qt.AlignCenter)
        pTextLabel.setWordWrap(True)
        pTextLabel.setTextInteractionFlags(Qt.NoTextInteraction)
        pTextLabel.setMouseTracking(False)
        pTextLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        pLayout.addWidget(pIconLabel)
        pLayout.addWidget(pTextLabel)
        
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
        
        #self.pb_multicell.setLayout(pLayout2)
        #self.pb_cav_database.setLayout(pLayout)   
        
##############################################################################
    # window with parameters definition (physics or geometric) --> Help window
    
    def click(self):
        widg=paramDef(self)
        widg.exec()
        
##############################################################################
    # close the main window      
    def Quit(self):
        self.close()
        
##############################################################################        

    def Open(self):
        widg=variableParam(self)
        widg.exec()
        
##############################################################################
#  define a new project in order to save all related files in a subfolder of BuildCav\
# subfolder defined by project name (Db folder, elmg_file folder and output folder)
# 1) DB folder --> db file containing HC and EG data
# 2) elmg_file --> Superfish files
# 3) outp_file --> multicell files

    def new_project(self):
        while True:
            self.path = normpath(str(QFileDialog.getExistingDirectory(self, "Choose project directory",'\\home\\BuildCav_2.0')))
            self.path_project=self.path    
            self.path_to_elmg_file=self.path
            
            if self.path == '.':
                break
            elif [y for y in [len(x.split(' ')) for x in self.path.split('\\')] if y > 1] != []:
                self.warning_wdj('Project folder can not have space in its name.')
            elif isdir(self.path + '\\outp_file'):
                self.warning_wdj('This project already exist. Create a new one.')
            else:
                scall('mkdir '+ self.path + '\\DB_file', shell=True)
                scall('mkdir '+ self.path + '\\elmg_file', shell=True)
                scall('mkdir '+ self.path + '\\outp_file', shell=True)
                
                self.name_project.setText('Project name: '+str((self.path.split('\\'))[len(self.path.split('\\'))-1]))
                self.name_project.setStyleSheet("background-color: lightgreen")
                break
            
##############################################################################        
# open an existing project

    def open_project(self):
        while True:
            self.path = normpath(str(QFileDialog.getExistingDirectory(self, "Choose project directory",'\\home\\BuildCav_2.0')))
            self.path_project=self.path    
            self.path_to_elmg_file=self.path

            if self.path == '.':
                break
            elif [y for y in [len(x.split(' ')) for x in self.path.split('\\')] if y > 1] != []:
                self.warning_wdj('Project folder can not have space in its name.')
            elif isdir(self.path + '\\outp_file') == False:
                self.warning_wdj('This project do not exist.')
            else:
                if isdir(self.path + '\\DB_file') == False:
                    scall('mkdir '+ self.path + '\\DB_file', shell=True)
                if isdir(self.path + '\\elmg_file') == False:
                    scall('mkdir '+ self.path + '\\elmg_file', shell=True)
                if isdir(self.path + '\\outp_file') == False:
                    scall('mkdir '+ self.path + '\\outp_file', shell=True)    
                self.name_project.setText('Project name: '+str((self.path.split('\\'))[len(self.path.split('\\'))-1]))
                self.name_project.setStyleSheet("background-color: lightgreen")
                break
                
##############################################################################        
# show buildCavity manual

    def show_info(self):
        try:
            url = QtCore.QUrl.fromLocalFile(getcwd()+"\\Guida.pdf")
            QtGui.QDesktopServices.openUrl(url)
        except:
            self.warning_wdj('Error: no guide opening')
            
##############################################################################        
# info about BuildCav development
     
    def show_about(self):
        messagebox = QMessageBox(parent = self)
        messagebox.setDefaultButton(QMessageBox.Ok)
        messagebox.setWindowTitle('About') 
        messagebox.setInformativeText("<style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Build Cavity2 1.0 </span></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The electromagnetic simulator for superconductive cavity. </p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Distributed under the  terms of <span style=\" font-style:italic;\">GNU GENERAL PUBLIC LICENSE</span>. </p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                 </p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Created by Alessio D\'Ambros, Milan, 2022, Elisa Del Core, Milan, 2022, a project of Paolo Pierini. Tested and debugged in collaboration with INFN LASA superconductive cavity group.</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">          </p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This project is part of a larger effort:</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    - Electromagnetic simulation solver:</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">        --&gt; <span style=\" font-style:italic;\">SuperFish</span> (website: https://laacg.lanl.gov/laacg/services/download_sf.phtml)</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">          </p>\n")
           
        info_logo = QPixmap(getcwd() + '\\logo.png')
        Pinfo_logo = info_logo.scaled(200, 200, Qt.KeepAspectRatio)
        messagebox.setIconPixmap(Pinfo_logo)
        messagebox.exec_()

 ##############################################################################        
 # show material properties (up to now, just that of Niobium)
        
    def set_material_properties(self):
         try:
             np.genfromtxt(getcwd() + '\\mat_prop.txt', dtype='str')
             widget_1 = Mat_Prop(self)
             widget_1.exec_()
             try:
                 self.mat_idx = widget_1.mat_idx
                 self.import_material()  
             except:
                 pass                      
         except:
             self.warning_wdj('Create a new project first!')

 ############################################################################## 
            
    def import_material(self):
        try:
            mat_list = np.genfromtxt(getcwd() + '\\mat_prop.txt', dtype='str').tolist()
            try:
                self.MATP = [float(x) for x in mat_list[self.mat_idx][1:len(mat_list[0])]]
                self.le_material.setText(mat_list[self.mat_idx][0])
            except:
                self.MATP = [float(x) for x in mat_list[1:len(mat_list)]]
                self.le_material.setText(mat_list[0])
            
            self.MATP[0] = self.MATP[0]/10**9    #---->  must be in kg/mm^3
            self.MATP[1] = self.MATP[1]*10**3    #---->  must be in MPa
            self.MATP[2] = self.MATP[2]*10**3    #---->  must be in MPa
            self.MATP[6] = self.MATP[6]/10**7    #---->  must be in Ohm/mm
            self.MATP[7] = self.MATP[7]/10**7    #---->  must be in Ohm/mm   
        except:
            self.MATP = np.array([8.57E-6, 1.06E+5, 1.18E+5, 0.4, 0.38, 50, 1.52e-05, 0, 0.00146])
            mat_list = np.array(['Niobium', 8570, 106, 118, 0.4, 0.38, 50, 152, 0, 0.00146])
            np.savetxt(getcwd() + '\\mat_prop.txt', mat_list, delimiter=" ", fmt="%s") 
            pass      

 ##############################################################################
 # define where to save all superfish files (define a folder or, with the newest modification, save them in project folder)
      
    def define_elmg_path(self, t):        
        if self.path_to_elmg_file == '':
            if t == 'function':
                self.warning_wdj('Select a folder where superfish file will be stored.') 
                
            while True:
                self.path_to_elmg_file = normpath(str(QFileDialog.getExistingDirectory(self, "Choose project directory",'\\home')))
                            
                if self.path_to_elmg_file == '.':
                    self.path_to_elmg_file = ''
                    break
                elif [y for y in [len(x.split(' ')) for x in self.path_to_elmg_file.split('\\')] if y > 1] != []:
                 self.warning_wdj('Project folder can not have space in its name.')
                else:
                    if self.tabWidget_2.currentIndex()==0:
                        if isdir(self.path_to_elmg_file + '\\elmg_file') == False:
                            scall('mkdir '+ self.path_to_elmg_file + '\\elmg_file', shell=True)
                        break
                    else:
                        break
                
##############################################################################                
   
    def convert_pg_param(self, n):
        if n == 0 and self.cb_geometric.isChecked() == True:
            self.frame_geometric.show()
            self.frame_phisic.hide()
            self.cb_geometric.setChecked(True)
            self.cb_physic.setChecked(False)
            if self.get_phisic() == 0:
                self.p2g()
            else:
                self.frame_geometric.hide()
                self.frame_phisic.show()
                self.cb_geometric.setChecked(False)
                self.cb_physic.setChecked(True)
                
        elif n == 0 and self.cb_geometric.isChecked() == False:
            self.cb_geometric.setChecked(True)
            
        elif n == 1 and self.cb_physic.isChecked() == True:
            self.frame_geometric.hide()
            self.frame_phisic.show()
            self.cb_geometric.setChecked(False)
            self.cb_physic.setChecked(True)
            if self.get_geom() == 0:
                self.g2p()
            else:
                self.frame_geometric.show()
                self.frame_phisic.hide()
                self.cb_geometric.setChecked(True)
                self.cb_physic.setChecked(False)
                
        elif n == 1 and self.cb_physic.isChecked() == True:
            self.cb_physic.setChecked(True)
                        
##############################################################################            
#### delete all values            
    def reset_pg_param(self):
        self.le_Sxeq.setText('')
        self.le_Syeq.setText('')
        self.le_Sxir.setText('')
        self.le_Syir.setText('')
        self.le_ER.setText('')
        self.le_IR.setText('')
        self.le_SL.setText('')
        self.le_IRpy.setText('')
        self.le_alpha.setText('')
        self.le_R.setText('')
        self.le_r.setText('')
        self.le_d.setText('')
        self.le_SLpy.setText('')
        self.le_H.setText('')
        self.le_f.setText('') # add
        self.le_LEQ.setText('') # add
        self.le_beta.setText('') # add
        self.figure.clf()
        self.canvas.draw()
        self.frame_sf_execution.hide()
            
##############################################################################
# get physics parameters --> read from GUI

    def get_phisic(self):  
        ok = 0
        try: 
            if self.le_IRpy.text() == '':
                self.CAV_py[0] = 2566196816216898
            else:
                self.CAV_py[0] = float(self.le_IRpy.text())
            if self.le_alpha.text() == '':
                self.CAV_py[1] = 2566196816216898
            else:            
                self.CAV_py[1] = float(self.le_alpha.text())
            if self.le_R.text() == '':
                self.CAV_py[2] = 2566196816216898
            else:                  
                self.CAV_py[2] = float(self.le_R.text())
            if self.le_r.text() == '':
                self.CAV_py[3] = 2566196816216898
            else:                  
                self.CAV_py[3] = float(self.le_r.text())
            if self.le_d.text() == '':
                self.CAV_py[4] = 2566196816216898
            else:                    
                self.CAV_py[4] = float(self.le_d.text())
            if self.le_SLpy.text() == '':
                self.CAV_py[5] = 2566196816216898                
            else:   
                self.CAV_py[5] = float(self.le_SLpy.text())
            if self.le_H.text() == '':
                self.CAV_py[6] = 2566196816216898                
            else:                       
                self.CAV_py[6] = float(self.le_H.text())
            if self.le_LEQ.text() == '':
                #self.CAV_py[7] = 2566196816216898
                self.new_parameter = 2566196816216898
            else:
                #self.CAV_py[7] = float(self.le_LEQ.text()) #Edited by Malini
                self.new_parameter = float(self.le_LEQ.text())
            
            if np.any(self.CAV_py) < 0:
                self.warning_wdj('To convert, all the 8 phisic parameters must be float positive numbers')
                ok = 1    
            if np.all(self.CAV_py == 2566196816216898):
                pass
            elif np.any(self.CAV_py == 2566196816216898):
                self.warning_wdj('To convert, all the 8 phisic parameters must be float positive numbers')
                ok = 1  
        except:
            self.warning_wdj('To convert, all the 8 phisical parameters must be float positive numbers')
            ok = 1

        return ok

##############################################################################
# convertion from physics to geometric parameters
       
    def p2g(self):
        try:
            if np.all(self.CAV_py == 2566196816216898):
                self.le_Sxeq.setText('')
                self.le_Syeq.setText('')
                self.le_Sxir.setText('')
                self.le_Syir.setText('')
                self.le_ER.setText('')
                self.le_IR.setText('')
                self.le_SL.setText('')
            else:  
                R_ir = self.CAV_py[0]
                alpha = self.CAV_py[1]*np.pi/180
                R = self.CAV_py[2]
                r = self.CAV_py[3]
                d = self.CAV_py[4]
                L = self.CAV_py[5]
                H = self.CAV_py[6]
                    
                geom=Geometry()
                A,B,a,b,R_eq=geom.p2g_geom(R_ir,alpha,R,r,d,L,H)
                self.le_Sxeq.setText(str(round(A,self.round_val)))
                self.le_Syeq.setText(str(round(B,self.round_val)))
                self.le_Sxir.setText(str(round(a,self.round_val)))
                self.le_Syir.setText(str(round(b,self.round_val)))
                self.le_ER.setText(str(round(R_eq,self.round_val)))
                self.le_IR.setText(str(round(R_ir,self.round_val)))
                self.le_SL.setText(str(round(L,self.round_val)))
                
                self.CAV_ge = np.array([A,B,a,b,R_eq,R_ir,L])
            
        except:
            self.frame_geometric.hide()
            self.frame_phisic.show()
            self.cb_geometric.setChecked(False)
            self.cb_physic.setChecked(True)
            self.warning_wdj("Can't convert this set of parameters.")

##############################################################################
# get geometric parameters --> read from GUI
            
    def get_geom(self):  
        ok = 0 
        try: 
            if self.le_Sxeq.text() == '':
                self.CAV_ge[0] = 2566196816216898
            else:
                self.CAV_ge[0] = float(self.le_Sxeq.text())
            if self.le_Syeq.text() == '':
                self.CAV_ge[1] = 2566196816216898
            else:            
                self.CAV_ge[1] = float(self.le_Syeq.text())
            if self.le_Sxir.text() == '':
                self.CAV_ge[2] = 2566196816216898
            else:                  
                self.CAV_ge[2] = float(self.le_Sxir.text())
            if self.le_Syir.text() == '':
                self.CAV_ge[3] = 2566196816216898
            else:                  
                self.CAV_ge[3] = float(self.le_Syir.text())
            if self.le_ER.text() == '':
                self.CAV_ge[4] = 2566196816216898
            else:                    
                self.CAV_ge[4] = float(self.le_ER.text())
            if self.le_IR.text() == '':
                self.CAV_ge[5] = 2566196816216898                
            else:   
                self.CAV_ge[5] = float(self.le_IR.text())
            if self.le_SL.text() == '':
                self.CAV_ge[6] = 2566196816216898                
            else:                       
                self.CAV_ge[6] = float(self.le_SL.text())
            if self.le_LEQ.text() == '':
                #self.CAV_ge[7] = 2566196816216898 # commented by Elisa
                self.new_parameter = 2566196816216898
            else:
                #self.CAV_ge[7] = float(self.le_LEQ.text()) #modified by Malini # commented by Elisa
                self.new_parameter = float(self.le_LEQ.text())

            if np.any(self.CAV_ge) < 0:
                self.warning_wdj('To convert, all the 8 geometric parameters must be float positive numbers')
                ok = 1
            if np.all(self.CAV_ge == 2566196816216898):
                pass
            elif np.any(self.CAV_ge == 2566196816216898):
                self.warning_wdj('To convert, all the 8 geometric parameters must be float positive numbers')
                ok = 1                
        except:
            self.warning_wdj('To convert, all the 8 geometric parameters must be float positive numbers')
            ok = 1

        return ok

##############################################################################
# convertion from geometric to physics parameters
            
    def g2p(self): 
        CAV = np.zeros((7))
        try:
            if np.all(self.CAV_ge == 2566196816216898):
                self.le_IRpy.setText('')
                self.le_alpha.setText('')
                self.le_R.setText('')
                self.le_r.setText('')
                self.le_d.setText('')
                self.le_SLpy.setText('')
                self.le_H.setText('')
            else:
                CAV[0] = self.CAV_ge[0]
                CAV[1] = self.CAV_ge[1]
                CAV[2] = self.CAV_ge[2]
                CAV[3] = self.CAV_ge[3]
                CAV[4] = self.CAV_ge[4]
                CAV[5] = self.CAV_ge[5]
                CAV[6] = self.CAV_ge[6]
                
                geom=Geometry()
                R_ir,alpha,R,r,d,L,H=geom.g2p_geom(CAV)

                self.le_IRpy.setText(str(round(R_ir,self.round_val)))
                self.le_alpha.setText(str(round(alpha,self.round_val)))
                self.le_R.setText(str(round(R,self.round_val)))
                self.le_r.setText(str(round(r,self.round_val)))
                self.le_d.setText(str(round(d,self.round_val)))
                self.le_SLpy.setText(str(round(L,self.round_val)))
                self.le_H.setText(str(round(H,self.round_val)))
                
                self.CAV_py = np.array([R_ir,alpha,R,r,d,L,H]) 
            
        except:
            self.frame_geometric.show()
            self.frame_phisic.hide()
            self.cb_geometric.setChecked(True)
            self.cb_physic.setChecked(False)
            self.warning_wdj("Can't convert this set of parameters.")            
    
##############################################################################
      
    def warning_wdj(self, text): # warning widget
        reply = QMessageBox.warning(
        self, "Warning", text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass    
        
                
    def critical_wdj(self, text): # error widget
        reply = QMessageBox.critical(
        self, "Critical error",
        text,
        QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            pass  

##############################################################################
# Draw cavity profile            
    def draw_cav(self):
        self.figure.clf()
        if self.tabWidget.currentIndex()==0:
            CAV = np.zeros((3,8))
            if self.cb_geometric.isChecked() == True and self.get_geom() == 0:
                CAV[0,0:7] = self.CAV_ge
                CAV[0,7] = 16
            elif self.cb_physic.isChecked() == True and self.get_phisic() == 0:
                self.p2g()
                CAV[0,0:7] = self.CAV_ge
                CAV[0,7] = 16
                   
            try:
                #x = Draw_cavity_profile('', CAV, 1) # old version before new_parameter
                x = Draw_cavity_profile_new('', CAV, 1, self.new_parameter,self)
                CAV_coo = x.CAV_coo()
                self.XC_param = x.XC_param

                if  len(CAV_coo) == 0:
                    self.critical_wdj('Unable to find ellipses tangent point due to unfeasible geometric parameters.')
                    self.frame_show_geom.hide()
                else:
                    add = np.array([[CAV_coo[-1,0],0],[0,0],[CAV_coo[0,0],CAV_coo[0,1]]])
                    CAV_coo = np.append(CAV_coo, add, axis = 0)
                    
                    self.figure.clf()
                    ax=self.figure.add_subplot(1,1,1)     
                    ax.plot(CAV_coo[:,0], CAV_coo[:,1], 'r-')
                    self.canvas.draw()
            except:
                self.warning_wdj('Unable to draw geometry.')    
        elif self.tabWidget.currentIndex()==1 or self.tabWidget.currentIndex()==3: # EG or SC
            self.draw_cav_EG()
        # elif self.tabWidget.currentIndex()==3:
        #     self.draw_cav_SC()
                   
##############################################################################           
############################################################################## 
############################################################################## 
# open cav database for half cell
            
    def open_cav_database(self): 
            
            if self.name_project.text()=='':
                self.warning_wdj('First, you must define a new project or open an existing one')
            else:
                cont=0
                try:
                    if self.le_Sxeq.text()!='':
                        self.CELL[0]=self.le_Sxeq.text()
                    else:
                        self.CELL[0]=0
                    if self.le_Syeq.text()!='':
                        self.CELL[1]=self.le_Syeq.text()
                    else:
                        self.CELL[1]=0
                    if self.le_Sxir.text()!='':
                        self.CELL[2]=self.le_Sxir.text()
                    else:
                        self.CELL[2]=0
                    if self.le_Syir.text()!='':
                        self.CELL[3]=self.le_Syir.text()
                    else:
                        self.CELL[3]=0
                    if self.le_ER.text()!='':
                        self.CELL[4]=self.le_ER.text()
                    else:
                        self.CELL[4]=0
                    if self.le_IR.text()!='':
                        self.CELL[5]=self.le_IR.text()
                    else:
                        self.CELL[5]=0
                    if self.le_SL.text()!='':
                        self.CELL[6]=self.le_SL.text()
                    else:
                        self.CELL[6]=0
                except:
                    self.CELL=np.zeros((7))
                for i in range(0,7):
                    if self.CELL[i]==0:
                        cont+=1
                        
                if cont==8:
                    try:
                        F_target = float(self.le_f.text())
                        if F_target < 0:
                            self.warning_wdj('Frequency target must be positive float number!')
                            ok = 1
                    except:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1            
                
                    if ok == 0 and self.path_to_elmg_file != '':
                        self.CELL = np.zeros((8))
                        if self.cb_geometric.isChecked() == True and self.get_geom() == 0:
                            self.CELL[0:7] = self.CAV_ge
                            self.CELL[7] = 18
                        elif self.cb_physic.isChecked() == True and self.get_phisic() == 0:
                            self.p2g()
                            self.CELL[0:7] = self.CAV_ge
                            self.CELL[7] = 18

                        emfn1=emfn()
                        self.beta=emfn1.def_beta_IC_EC(F_target, self.CELL)
                
                widget_2 = DB(self)
                widget_2.exec_()     
                
##############################################################################         
    # fill geometric parameters for half cell window
    def fill_g_param(self):           

        self.le_Sxeq.setText(str(round(self.CELL[0], self.round_val)))
        self.le_Syeq.setText(str(round(self.CELL[1], self.round_val)))
        self.le_Sxir.setText(str(round(self.CELL[2], self.round_val)))
        self.le_Syir.setText(str(round(self.CELL[3], self.round_val)))
        self.le_ER.setText(str(round(self.CELL[4], self.round_val)))
        self.le_IR.setText(str(round(self.CELL[5], self.round_val)))
        self.le_SL.setText(str(round(self.CELL[6], self.round_val)))
        self.draw_cav()
        self.frame_geometric.show()
        self.frame_phisic.hide()
        self.cb_geometric.setChecked(True)
        self.cb_physic.setChecked(False)
            
        
##############################################################################           
############################################################################## 
############################################################################## 
# Run first sf simulation (for half cell)
                
    def button_run_elmg_simulation(self):  
        if self.name_project.text()=='':
            self.warning_wdj('First, you must define a new project or open an existing one')
        else:
            self.define_elmg_path('function')
            ok = 0
            try:
                F_target = float(self.le_f.text())
                if F_target < 0:
                    self.warning_wdj('Frequency target must be positive float number!')
                    ok = 1
            except:
                self.warning_wdj('Frequency target must be positive float number!')
                ok = 1            
                 
            if ok == 0 and self.path_to_elmg_file != '':
                self.CELL = np.zeros((8))
                if self.cb_geometric.isChecked() == True and self.get_geom() == 0:
                    self.CELL[0:7] = self.CAV_ge
                    self.CELL[7] = 18
                elif self.cb_physic.isChecked() == True and self.get_phisic() == 0:
                    self.p2g()
                    self.CELL[0:7] = self.CAV_ge
                    self.CELL[7] = 18
                
                emfn1=emfn()
                self.beta=emfn1.def_beta_IC_EC(F_target, self.CELL)
    
                QApplication.setOverrideCursor(Qt.WaitCursor)
                
                try:
                    self.run_IC_sym(self.path_to_elmg_file, self.CELL, 500, self.CELL[2]/10, self.beta)
                    self.fill_elmg_parameters()
                    self.frame_sf_execution.show()
                except:
                    self.critical_wdj('Electromagnetic simulation error.')
                    self.frame_sf_execution.hide()
                    
                QApplication.restoreOverrideCursor() 

############################################################################
# fill the box with elmg parameters, from sf output file (for single cell)
            
    def fill_elmg_parameters(self):
        emfn1=emfn()
        sfo_file  = open(self.path_to_elmg_file+'\\elmg_file\\AF_file.SFO', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        
        self.SF_param = [0]*9
        f_pi = emfn1.Resonance_frequency(self.path_to_elmg_file)

        for k in range(len(cont)-1,0,-1):
            line = [x for x in cont[k].strip().split(' ') if x]
            try:
                if line[0] == 'Frequency':
                    self.SF_param[0] = str(f_pi)
                    self.SF_param[1] = line[-1]
                    break
                elif line[0] == 'Q':
                    self.SF_param[2] = line[2]
                elif line[0] == 'r/Q':
                    self.SF_param[3] = line[2]
                    self.SF_param[4] = line[3]
                if line[0] == 'Maximum' and line[1] == 'E': 
                    self.SF_param[5] = line[-4]          
                    line2 = [x for x in cont[k-1].strip().split(' ') if x]
                    self.SF_param[6] = line2[-4]  
            except:
                pass
 
        self.le_f.setText(self.SF_param[0])
        # lo tolgo da qui e lo sposto
        self.lb_se_f.setText('Frequency [' + self.SF_param[1] + '] = ' + self.SF_param[0])
            
        self.lb_se_q.setText('Q BCS factor @ 2K = ' + self.SF_param[2])
        self.lb_se_rq.setText('r/Q [' + self.SF_param[4] + '] = ' + self.SF_param[3]) 
        E_peak = float(self.SF_param[5])
        self.lb_se_E.setText('Epeak/Eacc =' + str(round(E_peak/10, self.round_val))) 
        H_peak = float(self.SF_param[6]) * 0.0012566370614359172
        self.lb_se_H.setText('Hpeak/Eacc [mT/(MV/m)] = ' + str(round(H_peak/10,self.round_val))) 
        
        af_old =  open(self.path_to_elmg_file+'\\elmg_file\\AF_file.AF', 'r')
        cont_af = af_old.readlines()
        af_old.close()  
        af_new =  open(self.path_to_elmg_file+'\\elmg_file\\AF_file.AF', 'w')
        cont_af[6] = 'nbslf=1, nbsrt=1, dslope =-1,\n'
        af_new.writelines(cont_af)
        af_new.close()                   
        scall(self.path_to_elmg_file+'\\elmg_file\\AF_file.AF', shell=True) # to run SuperFish
        f_0 = emfn1.Resonance_frequency(self.path_to_elmg_file)
        #self.SF_param[0]=str(f_0)
        #self.lb_se_f.setText('Frequency [' + self.SF_param[1] + '] = ' + self.SF_param[0])            
        K = (f_pi-f_0)/(0.5*(f_pi+f_0))    
        self.lb_se_K.setText('K [coupling, %] = ' + str(round(K*100,4))) 
        self.SF_param[7] = str(K)

        self.beta=emfn1.def_beta_IC_EC(f_pi,self.CELL)
        self.le_beta.setText(str(self.beta))
        self.SF_param[8] = str(self.beta)  

        self.le_f.setText(str(self.SF_param[0]))  
  
##############################################################################           
############################################################################## 
############################################################################## 
        
    def run_tuning(self):
        if self.tune_type == 'inner':
            self.tune_inner_cell()
        elif self.tune_type == 'end':
            self.tune_end_cell()    
      
##############################################################################    
    
# Tune inner cell --> only this one is used for half cell tuning, so the tune_end_cell is not used. It is
# mantained in this code just for simplicity. Then please refer only to tune_inner_cell for the HC tuning
        
    def tune_inner_cell(self):
        emfn1=emfn()
        if self.name_project.text()=='':
            self.warning_wdj('First, you must define a new project or open an existing one')
        else:
            self.define_elmg_path('function') 
            
            if self.path_to_elmg_file != '':
                ok = 0
                try:
                    F_target = float(self.le_f.text()) #initializes frequency target
                    if F_target < 0:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                    else:
                        widget_tune_parameters = Tune_parameters(self)
                        widget_tune_parameters.exec_() 
                        f_toll = widget_tune_parameters.f_toll
                except:
                    self.warning_wdj('Frequency target must be positive float number!')
                    ok = 1
            else:
                ok = 1
                
            if  ok == 0 and f_toll != 'cancel':  #initializes tuning tolerance
                self.CELL = np.zeros((8))
                if self.cb_geometric.isChecked() == True and self.get_geom() == 0:
                    self.CELL[0:7] = self.CAV_ge
                    self.CELL[7] = 16
                elif self.cb_physic.isChecked() == True and self.get_phisic() == 0:
                    self.p2g()
                    self.CELL[0:7] = self.CAV_ge
                    self.CELL[7] = 16
        
                dx = self.CELL[2]/10
                self.beta=emfn1.def_beta_IC_EC(F_target,self.CELL) #Calculates the beta value based on the target frequency
                self.le_beta.setText(str(self.beta))
                            
                X = [self.CELL[4]]
                D_b = self.CELL[4] + 10 
                
                QApplication.setOverrideCursor(Qt.WaitCursor)
               
                self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
                F  = [emfn1.Resonance_frequency(self.path_to_elmg_file) - F_target]
                
                self.CELL[4] = D_b
                self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
                f_b  = emfn1.Resonance_frequency(self.path_to_elmg_file) - F_target
                
                DF = (f_b-F[0])/(D_b-X[0])
                X += [X[0]-F[0]/DF]
                
                res = 10000
                k = 0
                while True:
                    self.CELL[4] = X[-1]  #in this while loop, the geometry is being updated, the frequency difference is alo being recalculated
                    self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
                    F += [emfn1.Resonance_frequency(self.path_to_elmg_file) - F_target]
                
                    DF = (F[-1]-F[-2])/(X[-1]-X[-2])
                    X += [X[-1]-F[-1]/DF]
                    
                    res = np.abs(F[-1]-F[-2])
            
                    k += 1
                    
                    if res < f_toll: #checks if res is within the frequency tolerance, if not the geometry updates until res falls within tolerance
                        break
                    
                    elif k > 100:
                        self.warning_wdj('Unable to find a feasible solution. Proces has been killed.')
                        break
    
                QApplication.restoreOverrideCursor() 
                
                self.CELL[4] = round(X[-1],self.round_val) # equatorial radius
                self.fill_elmg_parameters()
                self.frame_sf_execution.show()
                self.fill_g_param()

##############################################################################
            
# Tune end cell: don't refer to this one. It is not used.
        
    def tune_end_cell(self):  
        emfn1=emfn() 
        self.CELL[4] = self.new_equator_length
        self.le_equator_length.setText(str(self.CELL[4]))
        self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
        if self.name_project.text()=='':
            self.warning_wdj('First, you must define a new project or open an existing one')
        else:
            self.define_elmg_path('function') 
            
            if self.path_to_elmg_file != '':
                ok = 0
                try:
                    F_target = float(self.le_f.text())
                    if F_target < 0:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                    else:
                        widget_tune_parameters = Tune_parameters(self)
                        widget_tune_parameters.exec_() 
                        f_toll = widget_tune_parameters.f_toll
                except:
                    self.warning_wdj('Frequency target must be positive float number!')
                    ok = 1
            else:
                ok = 1
                
            if  f_toll != 'cancel' and ok == 0:
                self.CELL = np.zeros((8))
                if self.cb_geometric.isChecked() == True and self.get_geom() == 0:
                    self.CELL[0:7] = self.CAV_ge
                    self.CELL[7] = 16
                elif self.cb_physic.isChecked() == True and self.get_phisic() == 0:
                    self.p2g()
                    self.CELL[0:7] = self.CAV_ge
                    self.CELL[7] = 16
        
                dx = self.CELL[2]/10
                self.beta=emfn1.def_beta_IC_EC(F_target, self.CELL)
                self.le_beta.setText(str(self.beta))
                
                
                self.g2p()
                
                X = [self.CAV_py[1]]
                alpha_b = self.CAV_py[1] + 5 
                
                QApplication.setOverrideCursor(Qt.WaitCursor)
               
                self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
                F  = [emfn1.Resonance_frequency(self.path_to_elmg_file) - F_target]
            
                self.CAV_py[1] = alpha_b
                self.p2g()
                self.CELL = self.CAV_ge
                np.append(self.CELL, 16)
                self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
                f_b  = emfn1.Resonance_frequency(self.path_to_elmg_file) - F_target
                
                DF = (f_b-F[0])/(alpha_b-X[0])
                X += [X[0]-F[0]/DF]
                        
                res = 10000
                k = 0
                while True:
                    self.CAV_py[1] = X[-1]
                    self.p2g()
                    self.CELL = self.CAV_ge
                    np.append(self.CELL, 16)
                    self.run_IC_sym(self.path_to_elmg_file, self.CELL, F_target, dx, self.beta)
                    F += [emfn1.Resonance_frequency(self.path_to_elmg_file) - F_target]
                
                    DF = (F[-1]-F[-2])/(X[-1]-X[-2])
                    X += [X[-1]-F[-1]/DF]
                    
                    res = np.abs(F[-1]-F[-2])
            
                    k += 1
                    
                    if res < f_toll:
                        break
                    
                    elif k > 100:
                        self.warning_wdj('Unable to find a feasible solution. Proces has been killed.')
                        break
    
                QApplication.restoreOverrideCursor() 
                
                self.fill_elmg_parameters()
                self.frame_sf_execution.show()
                self.fill_g_param()
            
##############################################################################                     
# Half Cell SuperFish simulation
        
    def run_IC_sym(self, path, CELL, F_guess, dx, beta):
        if len(CELL) == 7:
            CELL = np.append(CELL, np.array([16]), axis = 0)
        CAV = np.zeros((3,8))
        CAV[0,:] = CELL
        IC = CELL
        #x = Draw_cavity_profile(path, CAV, 1.4)    # old 
        x = Draw_cavity_profile_new(path, CAV, 1.4, self.new_parameter,self)    

        geom=Geometry()
        Pic=geom.racc_point(IC)
        #Pic = x.racc_point(IC)
        e=Press_Button_ELMG_simulation(self.CAV, self.path,self) # set self in the input parameters if you want to recall parameters from
        # this class file into another one
        lines=e.IC_SF(F_guess, dx, IC, beta, Pic)       
               
        af_file =  open(path + '\\elmg_file\\AF_file.AF', 'w')           
        af_file.write('\n'.join(lines))
        af_file.close()
        
        scall(path+'\\elmg_file\\AF_file.AF', shell=True)
        
##############################################################################         
            
    def set_IC_EC_tune(self):      
        if self.tune_type == 'inner':
            self.tune_type = 'end'
            self.le_set_IC_EC.setText('END CELL TUNE')
            self.pb_set_IC_EC.setText('Inner Cell Tune') 
        elif self.tune_type == 'end':
            self.tune_type = 'inner'
            self.le_set_IC_EC.setText('INNER CELL TUNE')
            self.pb_set_IC_EC.setText('End Cell Tune')         
        
        self.reset_pg_param()
        self.frame_geometric.show()
        self.frame_phisic.hide()
        self.cb_geometric.setChecked(True)
        self.cb_physic.setChecked(False)
        self.frame_sf_execution.hide()
        
##############################################################################        
    
    def set_EG_tune(self):
        if self.name_project.text()=='':
            self.warning_wdj('First, you must define a new project or open an existing one')
        else:
            #widjet_1 = Tune_EG(self)
            #widjet_1.exec_()
            print('OK')
            
            #self.pathDB=widjet_1.Quit()            

##############################################################################
# End group trial: FROM HERE THE NEW LINE OF CODE
    
    # open db for end group
    def open_database(self):
        widget_IC = EndGroupDb(self, self.row1, self.row2)
        widget_IC.exec_()
        try:
            self.pathDB=widget_IC.button_cancel()
        except:        
            self.pathDB=widget_IC.button_ok()
    
    # definition of tube lengths
    def question(self):
        widget=info_Tube(self)
        widget.exec()
    
    # delete all values
    def reset_pg_param_2(self):
        self.le_f_2.setText('') # add
        self.le_beta_2.setText('') # add

        self.le_Sxeq_IC.setText('')
        self.le_Syeq_IC.setText('')
        self.le_Sxir_IC.setText('')
        self.le_Syir_IC.setText('')
        self.le_ER_IC.setText('')
        self.le_IR_IC.setText('')
        self.le_SL_IC.setText('')
        self.le_IRpy_IC.setText('')
        self.le_alpha_IC.setText('')
        self.le_R_IC.setText('')
        self.le_r_IC.setText('')
        self.le_d_IC.setText('')
        self.le_SLpy_IC.setText('')
        self.le_H_IC.setText('')
        self.le_LEQ_IC.setText('') # add
        
        self.le_Sxeq_EC.setText('')
        self.le_Syeq_EC.setText('')
        self.le_Sxir_EC.setText('')
        self.le_Syir_EC.setText('')
        self.le_ER_EC.setText('')
        self.le_IR_EC.setText('')
        self.le_SL_EC.setText('')
        self.le_IRpy_EC.setText('')
        self.le_alpha_EC.setText('')
        self.le_R_EC.setText('')
        self.le_r_EC.setText('')
        self.le_d_EC.setText('')
        self.le_SLpy_EC.setText('')
        self.le_H_EC.setText('')
        self.le_LEQ_EC.setText('') # add
            
##############################################################################
# Open database

    # inner cell db --> pen cell
    def click_Inner(self):
        widget_IC = InnerCell(self)
        widget_IC.exec_()
        self.row1=widget_IC.button_ok()
        if self.le_Sxeq_IC.text()!='':
            self.CAV_EG[0,0] = float(self.le_Sxeq_IC.text())
        else:
            self.CAV_EG[0,0] = 0
        if self.le_Syeq_IC.text()!='':
            self.CAV_EG[0,1] = float(self.le_Syeq_IC.text())
        else:
            self.CAV_EG[0,1] = 0
        if self.le_Sxir_IC.text()!='':
            self.CAV_EG[0,2] = float(self.le_Sxir_IC.text())    
        else:
            self.CAV_EG[0,2] = 0
        if self.le_Syir_IC.text()!='':
            self.CAV_EG[0,3] = float(self.le_Syir_IC.text())
        else:
            self.CAV_EG[0,3] = 0
        if self.le_ER_IC.text()!='':
            self.CAV_EG[0,4] = float(self.le_ER_IC.text())
        else:
            self.CAV_EG[0,4] = 0
        if self.le_IR_IC.text()!='':
            self.CAV_EG[0,5] = float(self.le_IR_IC.text())
        else:
            self.CAV_EG[0,5] = 0
        if self.le_SL_IC.text()!='':
            self.CAV_EG[0,6] = float(self.le_SL_IC.text())
        else:
            self.CAV_EG[0,6] = 0
        self.CAV[1,0:7] = self.CAV_EG[0,:]
        
    # end cell db
    def click_End(self):
        widget_EC=EndCell(self)
        widget_EC.exec()
        self.row2=widget_EC.button_ok()
        if self.le_Sxeq_EC.text()!='':
            self.CAV_EG[1,0] = float(self.le_Sxeq_EC.text())
        else:
            self.CAV_EG[1,0] = 0
        if self.le_Syeq_EC.text()!='':
            self.CAV_EG[1,1] = float(self.le_Syeq_EC.text())
        else:
            self.CAV_EG[1,1] = 0
        if self.le_Sxir_EC.text()!='':                 
            self.CAV_EG[1,2] = float(self.le_Sxir_EC.text())
        else:
            self.CAV_EG[1,2] = 0
        if self.le_Syir_EC.text()!='':                 
            self.CAV_EG[1,3] = float(self.le_Syir_EC.text())
        else:
            self.CAV_EG[1,3] = 0
        if self.le_ER_EC.text()!='':                  
            self.CAV_EG[1,4] = float(self.le_ER_EC.text())  
        else:
            self.CAV_EG[1,4] = 0
        if self.le_IR_EC.text()!='':
            self.CAV_EG[1,5] = float(self.le_IR_EC.text())
        else:
            self.CAV_EG[1,5]= 0
        if self.le_SL_EC.text()!='':                     
            self.CAV_EG[1,6] = float(self.le_SL_EC.text())
        else:
            self.CAV_EG[1,6]=0
        self.CAV[0,0:7] = self.CAV_EG[1,:]

##############################################################################

    # get physics paramters
    def get_phisic_2(self):  
        ok = 0
        try: 
                self.CAV_py_2[0,0] = float(self.le_IRpy_EC.text())       
                self.CAV_py_2[0,1] = float(self.le_alpha_EC.text())                  
                self.CAV_py_2[0,2] = float(self.le_R_EC.text())                 
                self.CAV_py_2[0,3] = float(self.le_r_EC.text())               
                self.CAV_py_2[0,4] = float(self.le_d_EC.text())
                self.CAV_py_2[0,5] = float(self.le_SLpy_EC.text())                    
                self.CAV_py_2[0,6] = float(self.le_H_EC.text())
                self.new_parameter_EC = float(self.le_LEQ_EC.text())
            
                self.CAV_py_2[2,0] = float(self.le_IRpy_IC.text())       
                self.CAV_py_2[2,1] = float(self.le_alpha_IC.text())                  
                self.CAV_py_2[2,2] = float(self.le_R_IC.text())                 
                self.CAV_py_2[2,3] = float(self.le_r_IC.text())               
                self.CAV_py_2[2,4] = float(self.le_d_IC.text())
                self.CAV_py_2[2,5] = float(self.le_SLpy_IC.text())                    
                self.CAV_py_2[2,6] = float(self.le_H_IC.text())
                self.new_parameter_IC = float(self.le_LEQ_IC.text())
        except:
            if self.le_Sxeq_EC.text() == '' or self.le_Sxeq_IC.text() == '':
                self.warning_wdj('Choose an inner and end cell first.')
            
            else:    
                self.warning_wdj('Corrupted cell. Check carefully cell database.')
            
            ok = 1

        return ok

    # physic to geometric parameters conversion
    def p2g_2(self, CAV_py, n):
        #try:
        R_ir = CAV_py[0]
        alpha = CAV_py[1]*np.pi/180
        R = CAV_py[2]
        r = CAV_py[3]
        d = CAV_py[4]
        L = CAV_py[5]
        H = CAV_py[6]
        
        geom=Geometry()
        A,B,a,b,R_eq=geom.p2g_geom(R_ir,alpha,R,r,d,L,H)

        if n == 0:
            self.le_Sxeq_EC.setText(str(round(A,self.round_val)))
            self.le_Syeq_EC.setText(str(round(B,self.round_val)))
            self.le_Sxir_EC.setText(str(round(a,self.round_val)))
            self.le_Syir_EC.setText(str(round(b,self.round_val)))
            self.le_ER_EC.setText(str(round(R_eq,self.round_val)))
            self.le_IR_EC.setText(str(round(R_ir,self.round_val)))
            self.le_SL_EC.setText(str(round(L,self.round_val)))
        
            if len(self.CAV_ge_2[0,:])==8:
                self.CAV_ge_2=np.delete(self.CAV_ge_2,7,1)
            self.CAV_ge_2[0,:] = np.array([A,B,a,b,R_eq,R_ir,L])
        
        elif n == 1:
            self.le_Sxeq_IC.setText(str(round(A,self.round_val)))
            self.le_Syeq_IC.setText(str(round(B,self.round_val)))
            self.le_Sxir_IC.setText(str(round(a,self.round_val)))
            self.le_Syir_IC.setText(str(round(b,self.round_val)))
            self.le_ER_IC.setText(str(round(R_eq,self.round_val)))
            self.le_IR_IC.setText(str(round(R_ir,self.round_val)))
            self.le_SL_IC.setText(str(round(L,self.round_val)))
        
            if len(self.CAV_ge_2[2,:])==8:
                self.CAV_ge_2=np.delete(self.CAV_ge_2,7,1)
            self.CAV_ge_2[2,:] = np.array([A,B,a,b,R_eq,R_ir,L])

    # read and save geoemtric parameters
    def get_geom_2(self):  
        ok = 0 
        try: 
                self.CAV_ge_2[0,0] = float(self.le_Sxeq_EC.text())            
                self.CAV_ge_2[0,1] = float(self.le_Syeq_EC.text())                 
                self.CAV_ge_2[0,2] = float(self.le_Sxir_EC.text())                 
                self.CAV_ge_2[0,3] = float(self.le_Syir_EC.text())                   
                self.CAV_ge_2[0,4] = float(self.le_ER_EC.text())  
                self.CAV_ge_2[0,5] = float(self.le_IR_EC.text())                       
                self.CAV_ge_2[0,6] = float(self.le_SL_EC.text())
                self.new_parameter_EC = float(self.le_LEQ_EC.text())

                self.CAV_ge_2[2,0] = float(self.le_Sxeq_IC.text())            
                self.CAV_ge_2[2,1] = float(self.le_Syeq_IC.text())                 
                self.CAV_ge_2[2,2] = float(self.le_Sxir_IC.text())                 
                self.CAV_ge_2[2,3] = float(self.le_Syir_IC.text())                   
                self.CAV_ge_2[2,4] = float(self.le_ER_IC.text())  
                self.CAV_ge_2[2,5] = float(self.le_IR_IC.text())                       
                self.CAV_ge_2[2,6] = float(self.le_SL_IC.text())
                self.new_parameter_IC = float(self.le_LEQ_IC.text())
                              
        except:
            if self.le_Sxeq_EC.text() == '' or self.le_Sxeq_IC.text() == '':
                self.warning_wdj('Choose an inner and end cell first.')
            else:   
                self.warning_wdj('Corrupted cell. Check carefully cell database.')
            ok = 1

        return ok

    # geometric to physic parameters conversion
    def g2p_2(self, CAV_ge, n): 
        CAV = np.zeros((7))
        CAV[0] = CAV_ge[0]
        CAV[1] = CAV_ge[1]
        CAV[2] = CAV_ge[2]
        CAV[3] = CAV_ge[3]
        CAV[4] = CAV_ge[4]
        CAV[5] = CAV_ge[5]
        CAV[6] = CAV_ge[6]

        geom=Geometry()
        R_ir,alpha,R,r,d,L,H=geom.g2p_geom(CAV)
  
        if n == 0:          
            self.le_IRpy_EC.setText(str(round(R_ir,self.round_val)))
            self.le_alpha_EC.setText(str(round(alpha,self.round_val)))
            self.le_R_EC.setText(str(round(R,self.round_val)))
            self.le_r_EC.setText(str(round(r,self.round_val)))
            self.le_d_EC.setText(str(round(d,self.round_val)))
            self.le_SLpy_EC.setText(str(round(L,self.round_val)))
            self.le_H_EC.setText(str(round(H,self.round_val)))
            
            self.CAV_py_2[0,:] = np.array([R_ir,alpha,R,r,d,L,H]) 
        
        elif n == 1:          
            self.le_IRpy_IC.setText(str(round(R_ir,self.round_val)))
            self.le_alpha_IC.setText(str(round(alpha,self.round_val)))
            self.le_R_IC.setText(str(round(R,self.round_val)))
            self.le_r_IC.setText(str(round(r,self.round_val)))
            self.le_d_IC.setText(str(round(d,self.round_val)))
            self.le_SLpy_IC.setText(str(round(L,self.round_val)))
            self.le_H_IC.setText(str(round(H,self.round_val)))
            
            self.CAV_py_2[2,:] = np.array([R_ir,alpha,R,r,d,L,H])    

    # conversion of parameters
    def convert_pg_param_2(self, n):
        if n == 0 and self.cb_geometric_2.isChecked() == True:
            self.frame_geometric_2.show()
            self.frame_phisic_2.hide()
            self.cb_geometric_2.setChecked(True)
            self.cb_physic_2.setChecked(False)
            if self.get_phisic_2() == 0:
                self.p2g_2(self.CAV_py_2[0,:],0)
                self.p2g_2(self.CAV_py_2[2,:],1)
            else:
                self.frame_geometric_2.hide()
                self.frame_phisic_2.show()
                self.cb_geometric_2.setChecked(False)
                self.cb_physic_2.setChecked(True)
                
        elif n == 0 and self.cb_geometric_2.isChecked() == False:
            self.cb_geometric_2.setChecked(True)
            
        elif n == 1 and self.cb_physic_2.isChecked() == True:
            self.frame_geometric_2.hide()
            self.frame_phisic_2.show()
            self.cb_geometric_2.setChecked(False)
            self.cb_physic_2.setChecked(True)
            if self.get_geom_2() == 0:
                self.g2p_2(self.CAV_ge_2[0,:],0)
                self.g2p_2(self.CAV_ge_2[2,:],1)
            else:
                self.frame_geometric_2.show()
                self.frame_phisic_2.hide()
                self.cb_geometric_2.setChecked(True)
                self.cb_physic_2.setChecked(False)
                
        elif n == 1 and self.cb_physic_2.isChecked() == True:
            self.cb_physic_2.setChecked(True)

    # check if the equator diameters of the PC and EC are equal
    def uniform_equator_diameter(self):
        reply = QMessageBox.question(self, '', "Pen and end cell have different equator diemeter. Do you want to rearrange pen cell equator diameter?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return 'yes'
        else:
            return 'no'  

    # run elmg simulation for EG
    def button_run_elmg_simulation_2(self):
        F_target=0
        emfn1=emfn()
        
        self.define_elmg_path('function')
        ok = 0
        try:
            F_target = float(self.le_f_2.text())
            if F_target < 0:
                self.warning_wdj('Frequency target must be positive float number!')
                ok = 1
        except:
            self.warning_wdj('Frequency target must be positive float number!')
            ok = 1   

        if ok == 0 and self.path_to_elmg_file != '':
            CAV = np.zeros((3,8))

            if self.cb_geometric_2.isChecked() == True and self.get_geom_2() == 0:
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]:
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.le_ER_IC.setText(str(self.CAV_ge_2[0,4]))
                        ok = 0
                    else:
                        ok = 1
                
            elif self.cb_physic_2.isChecked() == True and self.get_phisic_2() == 0:
                self.p2g_2(self.CAV_py_2[0,:], 0)
                self.p2g_2(self.CAV_py_2[2,:], 1)
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]: 
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.g2p(self.CAV_ge_2[2,:], 1)
                        ok = 0
                    else:
                        ok = 1   
                        
        if self.path_to_elmg_file != '':   
            if ok == 0 and self.get_tube_lenght(CAV) == 0:  
                CAV[1,-1] = float(self.le_tube_length.text())
                CAV[2,-1] = float(self.le_tube_length_Rir.text())        
            else: 
                ok = 1
                
            if ok == 0:  
                dx = CAV[0,2]/5
                self.beta=emfn1.def_beta_EG(F_target, CAV)
                self.le_beta_2.setText(str(self.beta))
            
            if F_target>0:
                try:
                    elmg_sim=self.button_run_elmg_simulation2_2(self.path_to_elmg_file, CAV, ok, F_target, dx)
                except Exception as E:
                    print(E)

                if path.exists(self.path_to_elmg_file+'\\elmg_file\\temp.txt'):   
                    try:
                        temp=open(self.path_to_elmg_file+'\\elmg_file\\temp.txt', 'r')
                        cont=temp.readlines()
                        freq=(cont[0].split(','))[0]
                        self.le_f_2.setText(freq)
                        self.le_beta_2.setText((cont[0].split(','))[1])
                        temp.close()
                        self.frame_sf_execution_2.show()
                        
                        self.lb_se_f_2.setText('Frequency [' + (cont[1].split(','))[1] + '] = ' + (cont[1].split(','))[0])            
                        self.lb_se_q_2.setText('Q BCS factor @ 2K = ' + (cont[1].split(','))[2])
                        self.lb_se_rq_2.setText('r/Q [' + (cont[1].split(','))[4] + '] = ' + (cont[1].split(','))[3]) 
                        self.lb_se_E_2.setText('Epeak/Eacc =' + (cont[1].split(','))[5])
                        self.lb_se_H_2.setText('Hpeak/Eacc [mT/(MV/m)] = ' + (cont[1].split(','))[6]) 
                        self.lb_se_K_2.setText('K [coupling, %] = ' + (cont[1].split(','))[7]) 
                        
                        self.tempArray[0,0]=float((cont[1].split(','))[0]) # freq
                        self.tempArray[0,1]=float((cont[1].split(','))[2]) # qbcs
                        self.tempArray[0,2]=float((cont[1].split(','))[3]) # r/q
                        self.tempArray[0,3]=float((cont[1].split(','))[5]) # e/eacc
                        self.tempArray[0,4]=float((cont[1].split(','))[6]) # h/eacc
                        self.tempArray[0,5]=float((cont[1].split(','))[7]) # k
                    except:
                        self.warning_wdj('Something went wrong')
                    remove(self.path_to_elmg_file+'\\elmg_file\\temp.txt')
                
                if path.exists(self.path_to_elmg_file+'\\elmg_file\\temp_tune.txt'):
                    CAV=self.CAV_tuning
                    self.fill_g_param_2(CAV) 

##########################################################################################
#### Electromagnetic simulation for end group from next line
    # run elmg simulation for EG                
    def button_run_elmg_simulation2_2(self,path_to_elmg_file, CAV, ok, F_target, dx):
        self.ok=ok
        self.CAV=CAV
        self.F_target=F_target
        self.path_to_elmg_file=path_to_elmg_file
        if self.ok == 0:
            QApplication.setOverrideCursor(Qt.WaitCursor)
        emfn1=emfn()
        try:
            self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
            self.run_EG_sym(self.path_to_elmg_file, self.CAV, 1000, self.CAV[0,2]/5, self.beta)
            if self.tabWidget.currentIndex() == 1: # EG
                self.frame_sf_execution_2.show()
            elif self.tabWidget.currentIndex() == 3: # SC
                self.frame_sf_execution_3.show()
            self.fill_elmg_parameters_2(self.CAV)
        except:
            self.critical_wdj('Electromagnetic simulation error.')
            if self.tabWidget.currentIndex() == 1: # EG
                self.frame_sf_execution_2.hide()
            elif self.tabWidget.currentIndex() == 3: # SC
                self.frame_sf_execution_3.hide()

        QApplication.restoreOverrideCursor()  
        
##############################################################################

    def run_EG_sym(self, path, CAV, F_guess, dx, beta):
        CAV[0,7] = 18
        #x = Draw_cavity_profile(path, CAV, 1.4) # old
        x = Draw_cavity_profile_new(path, CAV, 1.4, self.new_parameter,self)    
        IC = CAV[2,0:7]
        geom=Geometry()
        Pic=geom.racc_point(CAV[2,0:7])
        #Pic = x.racc_point(CAV[2,0:7])
        CAV[0,7] = 16
        #x = Draw_cavity_profile(path, CAV, 1.4)  # old
        x = Draw_cavity_profile_new(path, CAV, 1.4, self.new_parameter,self)   
        EC = CAV[0,0:7]
        Pec = geom.racc_point(CAV[0,0:7])
        #Pec = x.racc_point(CAV[0,0:7])
        
        l_tube = CAV[1,7]
        l_tube_Rir = CAV[2,7]
                 
        e=Press_Button_ELMG_simulation(self.CAV, self.path, self) #calc error
        lines=e.EG_SF(F_guess, dx, IC, beta, EC, Pic, Pec, l_tube_Rir, l_tube, CAV)
        
        af_file =  open(path + '\\elmg_file\\AF_file.AF', 'w')           
        af_file.write('\n'.join(lines))
        af_file.close()
        
        scall(path+'\\elmg_file\\AF_file.AF', shell=True)   
        
 ##############################################################################                    
    # fill elmg parameters computed through SuperFish for EG                     
    def fill_elmg_parameters_2(self, CAV):
        emfn1=emfn()
        sfo_file  = open(self.path_to_elmg_file+'\\elmg_file\\AF_file.SFO', 'r')
        cont = sfo_file.readlines()
        sfo_file.close()
        
        self.SF_param = [0]*9
        f_pi = emfn1.Resonance_frequency(self.path_to_elmg_file)

        for k in range(len(cont)-1,0,-1):
            line = [x for x in cont[k].strip().split(' ') if x]
            try:
                if line[0] == 'Frequency':
                    self.SF_param[0] = str(f_pi)
                    self.SF_param[1] = line[-1]
                    break
                elif line[0] == 'Q':
                    self.SF_param[2] = line[2]
                elif line[0] == 'r/Q':
                    self.SF_param[3] = line[2]
                    self.SF_param[4] = line[3]
                if line[0] == 'Maximum' and line[1] == 'E': 
                    self.SF_param[5] = line[-4]          
                    line2 = [x for x in cont[k-1].strip().split(' ') if x]
                    self.SF_param[6] = line2[-4]  
            except:
                pass
 
        # move the frequency setText below
        if self.tabWidget.currentIndex()==1: # EG
            self.le_f_2.setText(self.SF_param[0])
            self.lb_se_f_2.setText('Frequency [' + self.SF_param[1] + '] = ' + self.SF_param[0])            
            self.lb_se_q_2.setText('Q BCS factor @ 2K = ' + self.SF_param[2])
            self.lb_se_rq_2.setText('r/Q [' + self.SF_param[4] + '] = ' + self.SF_param[3]) 
            E_peak = float(self.SF_param[5])
            self.EpEacc=str(round(E_peak/10, self.round_val))
            self.lb_se_E_2.setText('Epeak/Eacc =' + str(round(E_peak/10, self.round_val))) 
            H_peak = float(self.SF_param[6]) * 0.0012566370614359172
            self.HpEacc=str(round(H_peak/10,self.round_val))
            self.lb_se_H_2.setText('Hpeak/Eacc [mT/(MV/m)] = ' + str(round(H_peak/10,self.round_val))) 
        elif self.tabWidget.currentIndex()==3: # SC
            self.le_f_3.setText(self.SF_param[0])
            self.lb_se_f_3.setText('Frequency [' + self.SF_param[1] + '] = ' + self.SF_param[0])            
            self.lb_se_q_3.setText('Q BCS factor @ 2K = ' + self.SF_param[2])
            self.lb_se_rq_3.setText('r/Q [' + self.SF_param[4] + '] = ' + self.SF_param[3]) 
            E_peak = float(self.SF_param[5])
            self.EpEacc=str(round(E_peak/10, self.round_val))
            self.lb_se_E_3.setText('Epeak/Eacc =' + str(round(E_peak/10, self.round_val))) 
            H_peak = float(self.SF_param[6]) * 0.0012566370614359172
            self.HpEacc=str(round(H_peak/10,self.round_val))
            self.lb_se_H_3.setText('Hpeak/Eacc [mT/(MV/m)] = ' + str(round(H_peak/10,self.round_val)))
        
        self.param_DB[0,1]=self.SF_param[0]
        self.param_DB[0,3]=str(round(E_peak/10, self.round_val))
        self.param_DB[0,4]=str(round(H_peak/10,self.round_val))
        self.param_DB[0,5]=self.SF_param[3]
        self.param_DB[0,6]=self.SF_param[2]
        
        af_old =  open(self.path_to_elmg_file+'\\elmg_file\\AF_file.AF', 'r')
        cont_af = af_old.readlines()
        af_old.close()  
        af_new =  open(self.path_to_elmg_file+'\\elmg_file\\AF_file.AF', 'w')
        cont_af[5] = 'nbslf=1, nbsrt=1, dslope =-1,\n'
        af_new.writelines(cont_af)
        af_new.close()                   
        scall(self.path_to_elmg_file+'\\elmg_file\\AF_file.AF', shell=True)
        f_0 = emfn1.Resonance_frequency(self.path_to_elmg_file)
        #self.SF_param[0]=str(f_0)
        #self.le_f_2.setText(self.SF_param[0])
        K = (f_pi-f_0)/(0.5*(f_pi+f_0))    
        if self.tabWidget.currentIndex()==1: # EG
            self.lb_se_f_2.setText('Frequency [' + self.SF_param[1] + '] = ' + self.SF_param[0])  
            self.lb_se_K_2.setText('K [coupling, %] = ' + str(round(K*100,self.round_val))) 
        elif self.tabWidget.currentIndex()==3: # SC
            self.lb_se_f_3.setText('Frequency [' + self.SF_param[1] + '] = ' + self.SF_param[0])            
            self.lb_se_K_3.setText('K [coupling, %] = ' + str(round(K*100,self.round_val))) 

        self.SF_param[7] = str(K)
        self.param_DB[0,7] = str(K)

        self.beta=emfn1.def_beta_EG(f_pi, CAV)
        if self.tabWidget.currentIndex()==1: # EG
            self.le_beta_2.setText(str(self.beta))
        elif self.tabWidget.currentIndex()==3: # SC
            self.le_beta_3.setText(str(self.beta))
        self.SF_param[8] = str(self.beta)    
        
        self.param_DB[0,2]=str(self.beta)

    # fill EG paramters values
    def fill_g_param_2(self, CAV): 

        if self.tabWidget.currentIndex() == 1: # EG
            self.le_Sxeq_EC.setText(str(round(CAV[0,0],self.round_val)))
            self.le_Syeq_EC.setText(str(round(CAV[0,1],self.round_val)))
            self.le_Sxir_EC.setText(str(round(CAV[0,2],self.round_val)))
            self.le_Syir_EC.setText(str(round(CAV[0,3],self.round_val)))
            self.le_ER_EC.setText(str(round(CAV[0,4],self.round_val)))
            self.le_IR_EC.setText(str(round(CAV[0,5],self.round_val)))
            self.le_SL_EC.setText(str(round(CAV[0,6],self.round_val)))
        
            self.le_Sxeq_IC.setText(str(round(CAV[2,0],self.round_val)))
            self.le_Syeq_IC.setText(str(round(CAV[2,1],self.round_val)))
            self.le_Sxir_IC.setText(str(round(CAV[2,2],self.round_val)))
            self.le_Syir_IC.setText(str(round(CAV[2,3],self.round_val)))
            self.le_ER_IC.setText(str(round(CAV[2,4],self.round_val)))
            self.le_IR_IC.setText(str(round(CAV[2,5],self.round_val)))
            self.le_SL_IC.setText(str(round(CAV[2,6],self.round_val)))
        elif self.tabWidget.currentIndex() == 3: # SC
            self.le_Sxeq_EC_2.setText(str(round(CAV[0,0],self.round_val)))
            self.le_Syeq_EC_2.setText(str(round(CAV[0,1],self.round_val)))
            self.le_Sxir_EC_2.setText(str(round(CAV[0,2],self.round_val)))
            self.le_Syir_EC_2.setText(str(round(CAV[0,3],self.round_val)))
            self.le_ER_EC_2.setText(str(round(CAV[0,4],self.round_val)))
            self.le_IR_EC_2.setText(str(round(CAV[0,5],self.round_val)))
            self.le_SL_EC_2.setText(str(round(CAV[0,6],self.round_val)))
        
            self.le_Sxeq_IC_2.setText(str(round(CAV[2,0],self.round_val)))
            self.le_Syeq_IC_2.setText(str(round(CAV[2,1],self.round_val)))
            self.le_Sxir_IC_2.setText(str(round(CAV[2,2],self.round_val)))
            self.le_Syir_IC_2.setText(str(round(CAV[2,3],self.round_val)))
            self.le_ER_IC_2.setText(str(round(CAV[2,4],self.round_val)))
            self.le_IR_IC_2.setText(str(round(CAV[2,5],self.round_val)))
            self.le_SL_IC_2.setText(str(round(CAV[2,6],self.round_val)))
        
        self.param_DB[0,8]=str(round(CAV[0,0],self.round_val))
        self.param_DB[0,9]=str(round(CAV[0,1],self.round_val))
        self.param_DB[0,10]=str(round(CAV[0,2],self.round_val))
        self.param_DB[0,11]=str(round(CAV[0,3],self.round_val))
        self.param_DB[0,12]=str(round(CAV[0,4],self.round_val))
        self.param_DB[0,13]=str(round(CAV[0,5],self.round_val))
        self.param_DB[0,14]=str(round(CAV[0,6],self.round_val))
        
        self.param_DB[0,15]=str(round(CAV[2,0],self.round_val))
        self.param_DB[0,16]=str(round(CAV[2,1],self.round_val))
        self.param_DB[0,17]=str(round(CAV[2,2],self.round_val))
        self.param_DB[0,18]=str(round(CAV[2,3],self.round_val))
        self.param_DB[0,19]=str(round(CAV[2,4],self.round_val))
        self.param_DB[0,20]=str(round(CAV[2,5],self.round_val))
        self.param_DB[0,21]=str(round(CAV[2,6],self.round_val))

        if self.tabWidget.currentIndex() == 1: # EG
            self.draw_cav_EG()
            self.frame_geometric_2.show()
            self.frame_phisic_2.hide()
            self.cb_geometric_2.setChecked(True)
            self.cb_physic_2.setChecked(False)
        if self.tabWidget.currentIndex() == 3: # SC
            self.frame_geometric_3.show()
            self.frame_phisic_3.hide()
            self.cb_geometric_3.setChecked(True)
            self.cb_physic_3.setChecked(False)
                       
##############################################################################                      
    # save tube length values        
    def get_tube_lenght(self, CAV):
        ok = 0
        
        try:
            if self.tabWidget.currentIndex()==1: # EG
                l1 = float((self.le_tube_length.text()).replace(' ',''))
                l2 = float((self.le_tube_length_Rir.text()).replace(' ',''))
            elif self.tabWidget.currentIndex()==3: # SC
                l1 = float((self.le_tube_length_2.text()).replace(' ',''))
                l2 = float((self.le_tube_length_Rir_2.text()).replace(' ',''))
        except:
            self.warning_wdj('Tube lengths must be positive float numbers.')    
            ok = 1
        
        if ok == 0:
            try:
                if l2 + np.abs(CAV[0,5]-CAV[2,5]) < l1:
                    CAV[1,7] = l1
                    CAV[2,7] = l2
                    self.param_DB[0,21]=l1
                    self.param_DB[0,22]=l2
                elif l2 == l1 and l1!=0:
                    self.warning_wdj('Tube lengths cannot be identicals')
                    ok = 1
                elif l2==l1 and l1==0:
                    CAV[1,7] = l1
                    CAV[2,7] = l2
                    self.param_DB[0,21]=l1
                    self.param_DB[0,22]=l2
                else:
                   self.warning_wdj('Cannot connect tube with different diameters.')      
                   ok = 1
            except:
                self.warning_wdj("Check tube lengths. Maybe not compatible lengths.")
        return ok
    
##############################################################################
    # choose the type of tuning
    def run_tuning_2(self):
        
        if self.tabWidget.currentIndex() == 1: # EG
            if self.rb_tune_alpha.isChecked():
                self.tune_with_alpha()
            elif self.rb_tune_req.isChecked():
                self.tune_with_Req()
            elif self.rb_tune_eql.isChecked():
                self.tune_with_EquatorLength()
            else:
                self.warning_wdj('Choose a tuning method')
        elif self.tabWidget.currentIndex() == 3: # SC
                if self.rb_tune_alpha_2.isChecked():
                    self.tune_with_alpha()
                elif self.rb_tune_req_2.isChecked():
                    self.tune_with_Req()
                else:
                    self.warning_wdj('Choose a tuning method')

    # tune with equator radius for EG and SC
    def tune_with_Req(self):
        
        if self.tabWidget.currentIndex() == 1: # EG
            freq=self.le_f_2.text()
        elif self.tabWidget.currentIndex() == 3: # SC
            freq=self.le_f_3.text()

        #if self.le_f_2.text() == '':
        if freq == '':
            self.warning_wdj('Please insert a valid frequency!')
        else:
            emfn1=emfn()
            if self.tabWidget.currentIndex() == 1: # EG
                self.F_target = float(self.le_f_2.text())
            elif self.tabWidget.currentIndex() == 3: # SC
                self.F_target = float(self.le_f_3.text())

            self.define_elmg_path('function')
    
            ok=0
            if ok == 0 and self.path_to_elmg_file != '':
                self.CAV = np.zeros((3,8))
                # if geometric parameters are filled 
                
                if self.tabWidget.currentIndex() == 1: # EG
                    if self.cb_geometric_2.isChecked() == True and self.get_geom_2() == 0:
                        self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                        self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                        self.CAV[0,7] = 19
                        if self.CAV[0,4] != self.CAV[2,4]:
                            if self.uniform_equator_diameter() == 'yes':
                                self.CAV[2,4] = self.CAV[0,4]
                                self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                                self.le_ER_IC.setText(str(self.CAV_ge_2[0,4]))
                                ok = 0
                            else:
                                ok = 1
                    # if physic parameters are filled
                    elif self.cb_physic_2.isChecked() == True and self.get_phisic_2() == 0:
                        self.p2g_2(self.CAV_py_2[0,:], 0)
                        self.p2g_2(self.CAV_py_2[2,:], 1)
                        self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                        self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                        self.CAV[0,7] = 19
                        if self.CAV[0,4] != self.CAV[2,4]: 
                            if self.uniform_equator_diameter() == 'yes':
                                self.CAV[2,4] = self.CAV[0,4]
                                self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                                self.g2p_2(self.CAV_ge_2[2,:], 1)
                                ok = 0
                            else:
                                ok = 1   
                
                elif self.tabWidget.currentIndex() == 3: # SC
                    if self.cb_geometric_3.isChecked() == True and self.get_geom_3() == 0:
                        self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                        self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                        self.CAV[0,7] = 19
                        if self.CAV[0,4] != self.CAV[2,4]:
                            if self.uniform_equator_diameter() == 'yes':
                                self.CAV[2,4] = self.CAV[0,4]
                                self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                                self.le_ER_IC_2.setText(str(self.CAV_ge_2[0,4]))
                                ok = 0
                            else:
                                ok = 1
                    # if physic parameters are filled
                    elif self.cb_physic_3.isChecked() == True and self.get_phisic_3() == 0:
                        self.p2g_3(self.CAV_py_2[0,:], 0)
                        self.p2g_3(self.CAV_py_2[2,:], 1)
                        self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                        self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                        self.CAV[0,7] = 19
                        if self.CAV[0,4] != self.CAV[2,4]: 
                            if self.uniform_equator_diameter() == 'yes':
                                self.CAV[2,4] = self.CAV[0,4]
                                self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                                self.g2p_3(self.CAV_ge_2[2,:], 1)
                                ok = 0
                            else:
                                ok = 1 
                            
            if self.path_to_elmg_file != '':   
                if ok == 0 and self.get_tube_lenght(self.CAV) == 0:  
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.CAV[1,-1] = float(self.le_tube_length.text())
                        self.CAV[2,-1] = float(self.le_tube_length_Rir.text())   
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.CAV[1,-1] = float(self.le_tube_length_2.text())
                        self.CAV[2,-1] = float(self.le_tube_length_Rir_2.text()) 
                else: 
                    ok = 1
                    
                if ok == 0:  
                    self.dx = self.CAV[0,2]/5
                    self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.le_beta_2.setText(str(self.beta))
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.le_beta_3.setText(str(self.beta))
            
            if self.path_to_elmg_file != '':
                ok = 0
                try:
                    if self.F_target < 0:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                    else:
                        widget_tune_parameters = Tune_parameters(self)
                        widget_tune_parameters.exec_() 
                        f_toll = widget_tune_parameters.f_toll
                except:
                    self.warning_wdj('Frequency target must be positive float number!')
                    ok = 1
            else:
                ok = 1
                
            if  ok == 0 and f_toll != 'cancel':            
                X = [self.CAV[0,4]]
                D_b = self.CAV[0,4] + 10 
                
                QApplication.setOverrideCursor(Qt.WaitCursor)
            
                self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
                self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                res=emfn1.Resonance_frequency(self.path_to_elmg_file)
                
                if res==self.F_target: # look at line 1248: to iterate the frequency for the tuning, it is calculated as the difference
                    # between emfn1.Resonance_frequency(self.path_to_elmg_file) and self.F_target. So the starting frequency must be different from the resonance frequency
                    # calculated with the resonance_frequency function
                    self.warning_wdj('Please insert a different starting frequency.')
                else:
                    F  = [res - self.F_target]
                    self.CAV[0,4] = D_b
                    self.CAV[2,4] = D_b
                    self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                    f_b  = emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target
                    
                    DF = (f_b-F[0])/(D_b-X[0])
                    X += [X[0]-F[0]/DF]
                    
                    res = 10000
                    k = 0
                    while True:
                        self.CAV[0,4] = X[-1]
                        self.CAV[2,4] = X[-1]
                        self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                        F += [emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target]
                    
                        DF = (F[-1]-F[-2])/(X[-1]-X[-2])
                        X += [X[-1]-F[-1]/DF]
                        
                        res = np.abs(F[-1]-F[-2])
                
                        k += 1
                        
                        if res < f_toll:
                            break
                        
                        elif k > 100:
                            self.warning_wdj('Unable to find a feasible solution. Proces has been killed.')
                            break
    
                    QApplication.restoreOverrideCursor() 
                    
                    self.CAV[0,4] = round(X[-1], 4)
                    self.CAV[2,4] = round(X[-1], 4)
                    self.CAV_ge_2 = np.asarray(self.CAV.tolist())
                    self.fill_elmg_parameters_2(self.CAV)
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.frame_sf_execution_2.show()
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.frame_sf_execution_3.show()
                    
                    self.CAV_tuning=self.CAV
                    self.fill_g_param_2(self.CAV)    
    
    # tune with alpha for both EG and SC
    def tune_with_alpha(self): 
        emfn1=emfn()

        ok=0
        f_toll=0

        if self.tabWidget.currentIndex() == 1: # EG
            if self.le_f_2.text() == '':
                self.warning_wdj('Please insert a valid frequency!')
            else:
                self.F_target = float(self.le_f_2.text())
                self.define_elmg_path('function') 
                ok=0
                if self.path_to_elmg_file != '':
                    ok = 0
                    try:
                        if self.F_target < 0:
                            self.warning_wdj('Frequency target must be positive float number!')
                            ok = 1
                        else:
                            widget_tune_parameters = Tune_parameters(self)
                            widget_tune_parameters.exec_() 
                            f_toll = widget_tune_parameters.f_toll
                    except:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                else:
                    ok = 1  


        if self.tabWidget.currentIndex() == 3: # SC
            if self.le_f_3.text() == '':
                self.warning_wdj('Please insert a valid frequency!')
            else:
                self.F_target = float(self.le_f_3.text())
                self.define_elmg_path('function') 
                ok=0
                if self.path_to_elmg_file != '':
                    ok = 0
                    try:
                        if self.F_target < 0:
                            self.warning_wdj('Frequency target must be positive float number!')
                            ok = 1
                        else:
                            widget_tune_parameters = Tune_parameters(self)
                            widget_tune_parameters.exec_() 
                            f_toll = widget_tune_parameters.f_toll
                    except:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                else:
                    ok = 1  


        if ok == 0 and self.path_to_elmg_file != '':
            self.CAV = np.zeros((3,8))


            if self.tabWidget.currentIndex() == 1: # EG
                if self.cb_geometric_2.isChecked() == True and self.get_geom_2() == 0:
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]:
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.le_ER_IC.setText(str(self.CAV_ge_2[0,4]))
                            ok = 0
                        else:
                            ok = 1
                    
                elif self.cb_physic_2.isChecked() == True and self.get_phisic_2() == 0:
                    self.p2g_2(self.CAV_py_2[0,:], 0)
                    self.p2g_2(self.CAV_py_2[2,:], 1)
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]: 
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.g2p_2(self.CAV_ge_2[2,:], 1)
                            ok = 0
                        else:
                            ok = 1   

            elif self.tabWidget.currentIndex() == 3: # SC
                if self.cb_geometric_3.isChecked() == True and self.get_geom_3() == 0:
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]:
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.le_ER_IC_2.setText(str(self.CAV_ge_2[0,4]))
                            ok = 0
                        else:
                            ok = 1
                    
                elif self.cb_physic_3.isChecked() == True and self.get_phisic_3() == 0:
                    self.p2g_3(self.CAV_py_2[0,:], 0)
                    self.p2g_3(self.CAV_py_2[2,:], 1)
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]: 
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.g2p_3(self.CAV_ge_2[2,:], 1)
                            ok = 0
                        else:
                            ok = 1   
                            
            if self.path_to_elmg_file != '':   
                if ok == 0 and self.get_tube_lenght(self.CAV) == 0:  
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.CAV[1,-1] = float(self.le_tube_length.text())
                        self.CAV[2,-1] = float(self.le_tube_length_Rir.text())   
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.CAV[1,-1] = float(self.le_tube_length_2.text())
                        self.CAV[2,-1] = float(self.le_tube_length_Rir_2.text())  
                else: 
                    ok = 1
                    
                if ok == 0:  
                    self.dx = self.CAV[0,2]/5
                    self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.le_beta_2.setText(str(self.beta))   
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.le_beta_3.setText(str(self.beta))
              
            if  ok == 0 and f_toll != 'cancel': 
                if self.tabWidget.currentIndex() == 1: # EG
                    self.g2p_2(self.CAV[0,:], 0)
                elif self.tabWidget.currentIndex() == 3: # SC
                    self.g2p_3(self.CAV[0,:], 0)
                   
                X = [self.CAV_py_2[0,1]]
                alpha_b = self.CAV_py_2[0,1] + 5 
               
                QApplication.setOverrideCursor(Qt.WaitCursor)
                
                self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
                self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                F  = [emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target]
           
                self.CAV_py_2[0,1] = alpha_b

                if self.tabWidget.currentIndex() == 1: # EG
                    self.p2g_2(self.CAV_py_2[0,:], 0)
                elif self.tabWidget.currentIndex() == 3: # SC
                    self.p2g_3(self.CAV_py_2[0,:], 0)
            
                self.CAV[0, 0:7] = self.CAV_ge_2[0, 0:7]
                self.CAV[2,4] = self.CAV_ge_2[0,4]
    
                self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                f_b  = emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target
               
                DF = (f_b-F[0])/(alpha_b-X[0])
                X += [X[0]-F[0]/DF]
                       
                res = 10000
                k = 0
                while True:
                    self.CAV_py_2[0,1] = X[-1]

                    if self.tabWidget.currentIndex() == 1: # EG
                        self.p2g_2(self.CAV_py_2[0,:], 0)
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.p2g_3(self.CAV_py_2[0,:], 0)                      
                    
                    self.CAV[0, 0:7] = self.CAV_ge_2[0, 0:7]
                    self.CAV[2,4] = self.CAV_ge_2[0,4]
    
                    self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                    F += [emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target]
               
                    DF = (F[-1]-F[-2])/(X[-1]-X[-2])
                    X += [X[-1]-F[-1]/DF]
                   
                    res = np.abs(F[-1]-F[-2])
           
                    k += 1
                   
                    if res < f_toll:
                        break
                   
                    elif k > 100:
                        self.warning_wdj('Unable to find a feasible solution. Process has been killed.')
                        break
        
                QApplication.restoreOverrideCursor() 
               
                self.fill_elmg_parameters_2(self.CAV)
                
                if self.tabWidget.currentIndex() == 1: # EG
                    self.frame_sf_execution_2.show()
                elif self.tabWidget.currentIndex() == 3: # SC
                    self.frame_sf_execution_3.show()

                self.CAV_tuning=self.CAV
                self.fill_g_param_2(self.CAV)

    def tune_with_EquatorLength(self):
        emfn1=emfn()
        ok=0
        f_toll=0

        if self.tabWidget.currentIndex() == 1: # EG
            if self.le_f_2.text() == '':
                self.warning_wdj('Please insert a valid frequency!')
            else:
                self.F_target = float(self.le_f_2.text())
                self.define_elmg_path('function') 
                ok=0
                if self.path_to_elmg_file != '':
                    ok = 0
                    try:
                        if self.F_target < 0:
                            self.warning_wdj('Frequency target must be positive float number!')
                            ok = 1
                        else:
                            widget_tune_parameters = Tune_parameters(self)
                            widget_tune_parameters.exec_() 
                            f_toll = widget_tune_parameters.f_toll
                    except:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                else:
                    ok = 1  


        if self.tabWidget.currentIndex() == 3: # SC
            if self.le_f_3.text() == '':
                self.warning_wdj('Please insert a valid frequency!')
            else:
                self.F_target = float(self.le_f_3.text())
                self.define_elmg_path('function') 
                ok=0
                if self.path_to_elmg_file != '':
                    ok = 0
                    try:
                        if self.F_target < 0:
                            self.warning_wdj('Frequency target must be positive float number!')
                            ok = 1
                        else:
                            widget_tune_parameters = Tune_parameters(self)
                            widget_tune_parameters.exec_() 
                            f_toll = widget_tune_parameters.f_toll
                    except:
                        self.warning_wdj('Frequency target must be positive float number!')
                        ok = 1
                else:
                    ok = 1  


        if ok == 0 and self.path_to_elmg_file != '':
            self.CAV = np.zeros((3,8))


            if self.tabWidget.currentIndex() == 1: # EG
                if self.cb_geometric_2.isChecked() == True and self.get_geom_2() == 0:
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]:
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.le_ER_IC.setText(str(self.CAV_ge_2[0,4]))
                            ok = 0
                        else:
                            ok = 1
                    
                elif self.cb_physic_2.isChecked() == True and self.get_phisic_2() == 0:
                    self.p2g_2(self.CAV_py_2[0,:], 0)
                    self.p2g_2(self.CAV_py_2[2,:], 1)
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]: 
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.g2p_2(self.CAV_ge_2[2,:], 1)
                            ok = 0
                        else:
                            ok = 1   

            elif self.tabWidget.currentIndex() == 3: # SC
                if self.cb_geometric_3.isChecked() == True and self.get_geom_3() == 0:
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]:
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.le_ER_IC_2.setText(str(self.CAV_ge_2[0,4]))
                            ok = 0
                        else:
                            ok = 1
                    
                elif self.cb_physic_3.isChecked() == True and self.get_phisic_3() == 0:
                    self.p2g_3(self.CAV_py_2[0,:], 0)
                    self.p2g_3(self.CAV_py_2[2,:], 1)
                    self.CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                    self.CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                    self.CAV[0,7] = 19
                    if self.CAV[0,4] != self.CAV[2,4]: 
                        if self.uniform_equator_diameter() == 'yes':
                            self.CAV[2,4] = self.CAV[0,4]
                            self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                            self.g2p_3(self.CAV_ge_2[2,:], 1)
                            ok = 0
                        else:
                            ok = 1   
                            
            if self.path_to_elmg_file != '':   
                if ok == 0 and self.get_tube_lenght(self.CAV) == 0:  
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.CAV[1,-1] = float(self.le_tube_length.text())
                        self.CAV[2,-1] = float(self.le_tube_length_Rir.text())   
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.CAV[1,-1] = float(self.le_tube_length_2.text())
                        self.CAV[2,-1] = float(self.le_tube_length_Rir_2.text())  
                else: 
                    ok = 1
                    
                if ok == 0:  
                    self.dx = self.CAV[0,2]/5
                    self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
                    if self.tabWidget.currentIndex() == 1: # EG
                        self.le_beta_2.setText(str(self.beta))   
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.le_beta_3.setText(str(self.beta))
              
            if  ok == 0 and f_toll != 'cancel': 
                if self.tabWidget.currentIndex() == 1: # EG
                    self.g2p_2(self.CAV[0,:], 0)
                elif self.tabWidget.currentIndex() == 3: # SC
                    self.g2p_3(self.CAV[0,:], 0)
                   
                E_X = [self.LEQ]
                E_D_b = self.LEQ + 1 
               
                QApplication.setOverrideCursor(Qt.WaitCursor)
                
                self.beta=emfn1.def_beta_EG(self.F_target, self.CAV)
                self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                F  = [emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target]
           
                self.CAV_py_2[0,1] = E_D_b

                if self.tabWidget.currentIndex() == 1: # EG
                    self.p2g_2(self.CAV_py_2[0,:], 0)
                elif self.tabWidget.currentIndex() == 3: # SC
                    self.p2g_3(self.CAV_py_2[0,:], 0)
            
                self.CAV[0, 0:7] = self.CAV_ge_2[0, 0:7]
                self.CAV[2,4] = self.CAV_ge_2[0,4]
    
                self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                f_b  = emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target
               
                DF = (f_b-F[0])/(E_D_b-X[0])
                E_X += [X[0]-F[0]/DF]
                       
                res = 10000
                k = 0
                while True:
                    self.CAV_py_2[0,1] = X[-1]

                    if self.tabWidget.currentIndex() == 1: # EG
                        self.p2g_2(self.CAV_py_2[0,:], 0)
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.p2g_3(self.CAV_py_2[0,:], 0)                      
                    
                    self.CAV[0, 0:7] = self.CAV_ge_2[0, 0:7]
                    self.CAV[2,4] = self.CAV_ge_2[0,4]
    
                    self.run_EG_sym(self.path_to_elmg_file, self.CAV, self.F_target, self.dx, self.beta)
                    F += [emfn1.Resonance_frequency(self.path_to_elmg_file) - self.F_target]
               
                    DF = (F[-1]-F[-2])/(X[-1]-X[-2])
                    X += [X[-1]-F[-1]/DF]
                   
                    res = np.abs(F[-1]-F[-2])
           
                    k += 1
                   
                    if res < f_toll:
                        break
                   
                    elif k > 100:
                        self.warning_wdj('Unable to find a feasible solution. Process has been killed.')
                        break
        
                QApplication.restoreOverrideCursor() 
               
                self.fill_elmg_parameters_2(self.CAV)
                
                if self.tabWidget.currentIndex() == 1: # EG
                    self.frame_sf_execution_2.show()
                elif self.tabWidget.currentIndex() == 3: # SC
                    self.frame_sf_execution_3.show()

                self.CAV_tuning=self.CAV
                self.fill_g_param_2(self.CAV)

##############################################################################
    # draw the profile of the end group and of the single cell
    
    def draw_cav_EG(self):
        ok = 0
        CAV = np.zeros((3,8))
        
        if self.tabWidget.currentIndex() == 1: # EG
            if self.cb_geometric_2.isChecked() == True and self.get_geom_2() == 0:
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]:
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.le_ER_IC.setText(str(self.CAV_ge_2[0,4]))
                        ok = 0
                    else:
                        ok = 1
                
            elif self.cb_physic_2.isChecked() == True and self.get_phisic_2() == 0:
                self.p2g_2(self.CAV_py_2[0,:], 0)
                self.p2g_2(self.CAV_py_2[2,:], 1)
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]: 
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.g2p_2(self.CAV_ge_2[2,:], 1)
                        ok = 0
                    else:
                        ok = 1    

        elif self.tabWidget.currentIndex() == 3: # SC
            if self.cb_geometric_3.isChecked() == True and self.get_geom_3() == 0:
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]:
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.le_ER_IC_2.setText(str(self.CAV_ge_2[0,4]))
                        ok = 0
                    else:
                        ok = 1
                
            elif self.cb_physic_3.isChecked() == True and self.get_phisic_3() == 0:
                self.p2g_2(self.CAV_py_2[0,:], 0)
                self.p2g_2(self.CAV_py_2[2,:], 1)
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]: 
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.g2p_3(self.CAV_ge_2[2,:], 1)
                        ok = 0
                    else:
                        ok = 1  
            
            
        if self.get_tube_lenght(CAV) == 0 and ok == 0:
            try:         
                if self.tabWidget.currentIndex() == 1: # EG
                    l1 = float(self.le_tube_length.text())
                    l2 = float(self.le_tube_length_Rir.text())
                elif self.tabWidget.currentIndex() == 3: # SC
                    l1 = float(self.le_tube_length_2.text())
                    l2 = float(self.le_tube_length_Rir_2.text())
                IC_EG = np.zeros((3,8))
                IC_EG[0,:] = CAV[2,:]
                IC_EG[0,7] = 16
                if self.path_to_elmg_file!='':
                    if self.tabWidget.currentIndex() == 1: # EG
                        #widget_draw=draw(self, IC_EG, l1, l2, CAV, self.path_to_elmg_file)
                        self.draw_new_EG(IC_EG, l1, l2, CAV, self.path_to_elmg_file)
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.draw_new_SC(IC_EG, l1, l2, CAV, self.path_to_elmg_file)
                else:
                    if self.tabWidget.currentIndex() == 1: # EG
                        # widget_draw=draw(self, IC_EG, l1, l2, CAV, getcwd()) 
                        self.draw_new_EG(IC_EG, l1, l2, CAV, getcwd())
                    elif self.tabWidget.currentIndex() == 3: # SC
                        self.draw_new_SC(IC_EG, l1, l2, CAV, getcwd())
                #widget_draw.exec()
            except:
                self.warning_wdj('Unable to draw geometry.')

    def draw_new_EG(self,IC_EG,l1,l2,CAV,path_to_elmg_file): # to draw the EG profile
        try:
            #x = Draw_cavity_profile('', IC_EG, 1) # old commentato 17 01 2025
            x = Draw_cavity_profile_new('', IC_EG, 1, self.new_parameter_IC,self)

            IC_coo = x.CAV_coo()
            IC_coo[:,0] = -IC_coo[:,0] + IC_coo[-1,0] 
            IC_coo[:,0] = np.flip(IC_coo[:,0])
            IC_coo[:,1] = np.flip(IC_coo[:,1])

            self.EC_EG = np.zeros((3,8))
            self.EC_EG[0,:] = CAV[0,:]
            self.EC_EG[0,7] = 16
            #x = Draw_cavity_profile('', self.EC_EG, 1) # old
            x = Draw_cavity_profile_new('', self.EC_EG, 1, self.new_parameter_EC,self)
            EC_coo = x.CAV_coo()
            EC_coo[:,0] = EC_coo[:,0] + IC_coo[-1,0]
        
            CAV_coo = np.append(IC_coo, EC_coo, axis = 0)
            end = CAV_coo[-1,0]
            
            if l2 == 0:
                add = np.array([[end + l1, CAV_coo[-1,1]],
                                [end + l1, 0],
                                [0,0],
                                [CAV_coo[0,0], CAV_coo[0,1]]])
            else:
                add = np.array([[end + l2, CAV_coo[-1,1]],
                                [end + l2 + np.abs(CAV[0,5]-CAV[2,5]), CAV_coo[0,1]],
                                [end + l1, CAV_coo[0,1]],
                                [end + l1, 0],
                                [0,0],
                                [CAV_coo[0,0], CAV_coo[0,1]]])
            CAV_coo = np.append(CAV_coo, add, axis = 0)


            ax=self.figure.add_subplot(1,1,1)     
            ax.plot(CAV_coo[:,0], CAV_coo[:,1], 'r-')
            self.canvas.draw()

            # old
            #fig,ax = plt.subplots(1)
            #ax.axis('off')
            #plt.plot(CAV_coo[:,0], CAV_coo[:,1], color='r')
            l=''
            file=open(path_to_elmg_file+"\\fileDraw.txt",'w')
            for i in range(len(CAV_coo)):
                l+=str(CAV_coo[i,0])+','+str(CAV_coo[i,1])+'\n'
            file.write(l)
            file.close()
            plt.savefig(path_to_elmg_file+"\\fileDraw.png")
        except:
            self.warning_wdj('Something wrong during the cavity profile definition')

###############################################################################
# MULTICELL

    def button_init_M(self):
        MW_path = getcwd()


    # check the radius of the half cell iris and that of PC (pen cell) of end group: they must be equal
    def Superfish_execution_M(self):

        self.CAV = np.zeros((5,8))
        self.nameIC = self.cb_InnerCell.currentText()
        self.nameEG1 = self.cb_EndGroup1.currentText()
        self.nameEG2 = self.cb_EndGroup2.currentText()
        
        # IC
        
        file1=open(self.pathDB,'r')
        line1=file1.readlines()
        file1.close()
        
        # read db data to fill the tables with half cells and end groups in order to choose
        # and combine them to find out the multicell
        for i in range(len(line1)):
            if not line1[i].startswith('\n'):
                try:
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
                except:
                    self.warning_wdj('Please check if there are empty parameters')
                    break

        if self.CAV[1,5]==self.CAV[2,5]:

            #### Superfish for the multicell
            numberCell = 0
            contSuper=0
            try:
                if self.textEdit_NumberCell_2.text()!='':
                    
                    if not str(self.textEdit_NumberCell_2.text()).isdigit():
                        self.warning_wdj('The number of cells must be a valid integer number')
                    elif not float(self.textEdit_NumberCell_2.text()).is_integer():
                            self.warning_wdj('The number of cells must be an integer number')
                    else:
                        numberCells=int(self.textEdit_NumberCell_2.text().replace(' ','').replace('\t','').replace('\n','').replace('  ',''))
                        self.CAV[0,7] = numberCells
                        contSuper+=1
                else:
                    self.warning_wdj('Please insert a number of cells')
                    
            except:
                self.warning_wdj('Errors reading Number Cells')
            
            self.elmg_param[0,1]=self.CAV[0,4]/20
            
            path=self.path

            if contSuper==1:
                self.define_elmg_path('function')
                path=self.path
                elmg_sym=Press_Button_ELMG_simulation(self.CAV, self.path)
                elmg_sym.run_elmg_simulation()
                pathFile=path+'\\elmg_file\\log_coo_base.txt'

                            
                file=open(pathFile,'r')
                x=[]
                y=[]
                line=file.readlines()
                file.close()
                for i in range(len(line)):
                    t=re.sub('\\s+',';',line[i])
                    s=t.split(';')
                    x.append(float(s[3]))
                    y.append(float(s[4]))

                fig1=plt.figure()
                plt.plot(x, y, color='red')
                plt.axis('equal')
                fig1.savefig(path+"\\figProfile.png")
                
                
                self.figure2.clf()
                ax=self.figure2.add_subplot(1,1,1)     
                ax.plot(x, y, 'r-')
                self.canvas2.draw()     
                
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
                except:
                    self.critical_wdj = ('Error reading AF_FILE.SFO file.') 

            if contSuper==1:
                #Cavity output
                widget_output = cavityOutput(self, self.CAV, path, self.peaks, self.output_file)
                widget_output.exec_()
        else:
            self.warning_wdj('The iris radius of half cell and that of pen cell used to build the end group must be equal') 

    # field data from TBL
    def field_data(self, path):     
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
            t=re.sub('\\s+',';',line[i])
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
#### Single Cell

# reset all the parameters values
    def reset_pg_param_3(self):
        self.le_f_3.setText('') # add
        self.le_beta_3.setText('') # add

        self.le_Sxeq_IC_2.setText('')
        self.le_Syeq_IC_2.setText('')
        self.le_Sxir_IC_2.setText('')
        self.le_Syir_IC_2.setText('')
        self.le_ER_IC_2.setText('')
        self.le_IR_IC_2.setText('')
        self.le_SL_IC_2.setText('')
        self.le_IRpy_IC_2.setText('')
        self.le_alpha_IC_2.setText('')
        self.le_R_IC_2.setText('')
        self.le_r_IC_2.setText('')
        self.le_d_IC_2.setText('')
        self.le_SLpy_IC_2.setText('')
        self.le_H_IC_2.setText('')
        self.le_SL_IC_2.setText('') # add
        
        self.le_Sxeq_EC_2.setText('')
        self.le_Syeq_EC_2.setText('')
        self.le_Sxir_EC_2.setText('')
        self.le_Syir_EC_2.setText('')
        self.le_ER_EC_2.setText('')
        self.le_IR_EC_2.setText('')
        self.le_SL_EC_2.setText('')
        self.le_IRpy_EC_2.setText('')
        self.le_alpha_EC_2.setText('')
        self.le_R_EC_2.setText('')
        self.le_r_EC_2.setText('')
        self.le_d_EC_2.setText('')
        self.le_SLpy_EC_2.setText('')
        self.le_H_EC_2.setText('')
        self.le_SL_EC_2.setText('') # add

        self.le_tube_length_2.setText('')
        self.le_tube_length_Rir_2.setText('')

##############################################################################
# Open database: inner and end cell

    def click_Inner2(self):
        widget_IC = InnerCell2(self)
        widget_IC.exec_()
        self.row1=widget_IC.button_ok()
        if self.le_Sxeq_IC_2.text()!='':
            self.CAV_EG[0,0] = float(self.le_Sxeq_IC_2.text())
        else:
            self.CAV_EG[0,0] = 0
        if self.le_Syeq_IC_2.text()!='':
            self.CAV_EG[0,1] = float(self.le_Syeq_IC_2.text())
        else:
            self.CAV_EG[0,1] = 0
        if self.le_Sxir_IC_2.text()!='':
            self.CAV_EG[0,2] = float(self.le_Sxir_IC_2.text())    
        else:
            self.CAV_EG[0,2] = 0
        if self.le_Syir_IC_2.text()!='':
            self.CAV_EG[0,3] = float(self.le_Syir_IC_2.text())
        else:
            self.CAV_EG[0,3] = 0
        if self.le_ER_IC_2.text()!='':
            self.CAV_EG[0,4] = float(self.le_ER_IC_2.text())
        else:
            self.CAV_EG[0,4] = 0
        if self.le_IR_IC_2.text()!='':
            self.CAV_EG[0,5] = float(self.le_IR_IC_2.text())
        else:
            self.CAV_EG[0,5] = 0
        if self.le_SL_IC_2.text()!='':
            self.CAV_EG[0,6] = float(self.le_SL_IC_2.text())
        else:
            self.CAV_EG[0,6] = 0
        self.CAV[1,0:7] = self.CAV_EG[0,:]
        

    def click_End2(self):
        widget_EC=EndCell2(self)
        widget_EC.exec()
        self.row2=widget_EC.button_ok()
        if self.le_Sxeq_EC_2.text()!='':
            self.CAV_EG[1,0] = float(self.le_Sxeq_EC_2.text())
        else:
            self.CAV_EG[1,0] = 0
        if self.le_Syeq_EC_2.text()!='':
            self.CAV_EG[1,1] = float(self.le_Syeq_EC_2.text())
        else:
            self.CAV_EG[1,1] = 0
        if self.le_Sxir_EC_2.text()!='':                 
            self.CAV_EG[1,2] = float(self.le_Sxir_EC_2.text())
        else:
            self.CAV_EG[1,2] = 0
        if self.le_Syir_EC_2.text()!='':                 
            self.CAV_EG[1,3] = float(self.le_Syir_EC_2.text())
        else:
            self.CAV_EG[1,3] = 0
        if self.le_ER_EC_2.text()!='':                  
            self.CAV_EG[1,4] = float(self.le_ER_EC_2.text())  
        else:
            self.CAV_EG[1,4] = 0
        if self.le_IR_EC_2.text()!='':
            self.CAV_EG[1,5] = float(self.le_IR_EC_2.text())
        else:
            self.CAV_EG[1,5]= 0
        if self.le_SL_EC_2.text()!='':                     
            self.CAV_EG[1,6] = float(self.le_SL_EC_2.text())
        else:
            self.CAV_EG[1,6]=0
        self.CAV[0,0:7] = self.CAV_EG[1,:]

########################
# convert
    def convert_pg_param_3(self, n):
        if n == 0 and self.cb_geometric_3.isChecked() == True:
            self.frame_geometric_3.show()
            self.frame_phisic_3.hide()
            self.cb_geometric_3.setChecked(True)
            self.cb_physic_3.setChecked(False)
            if self.get_phisic_3() == 0:
                self.p2g_3(self.CAV_py_2[0,:],0)
                self.p2g_3(self.CAV_py_2[2,:],1)
            else:
                self.frame_geometric_3.hide()
                self.frame_phisic_3.show()
                self.cb_geometric_3.setChecked(False)
                self.cb_physic_3.setChecked(True)
                
        elif n == 0 and self.cb_geometric_3.isChecked() == False:
            self.cb_geometric_3.setChecked(True)
            
        elif n == 1 and self.cb_physic_3.isChecked() == True:
            self.frame_geometric_3.hide()
            self.frame_phisic_3.show()
            self.cb_geometric_3.setChecked(False)
            self.cb_physic_3.setChecked(True)
            if self.get_geom_3() == 0:
                self.g2p_3(self.CAV_ge_2[0,:],0)
                self.g2p_3(self.CAV_ge_2[2,:],1)
            else:
                self.frame_geometric_3.show()
                self.frame_phisic_3.hide()
                self.cb_geometric_3.setChecked(True)
                self.cb_physic_3.setChecked(False)
                
        elif n == 1 and self.cb_physic_3.isChecked() == True:
            self.cb_physic_3.setChecked(True)

##############################################################################
    # get physic parameters --> read physic parameters
    def get_phisic_3(self):  
        ok = 0
        try: 
                self.CAV_py_2[0,0] = float(self.le_IRpy_EC_2.text())       
                self.CAV_py_2[0,1] = float(self.le_alpha_EC_2.text())                  
                self.CAV_py_2[0,2] = float(self.le_R_EC_2.text())                 
                self.CAV_py_2[0,3] = float(self.le_r_EC_2.text())               
                self.CAV_py_2[0,4] = float(self.le_d_EC_2.text())
                self.CAV_py_2[0,5] = float(self.le_SLpy_EC_2.text())                    
                self.CAV_py_2[0,6] = float(self.le_H_EC_2.text())
            
                self.CAV_py_2[2,0] = float(self.le_IRpy_IC_2.text())       
                self.CAV_py_2[2,1] = float(self.le_alpha_IC_2.text())                  
                self.CAV_py_2[2,2] = float(self.le_R_IC_2.text())                 
                self.CAV_py_2[2,3] = float(self.le_r_IC_2.text())               
                self.CAV_py_2[2,4] = float(self.le_d_IC_2.text())
                self.CAV_py_2[2,5] = float(self.le_SLpy_IC_2.text())                    
                self.CAV_py_2[2,6] = float(self.le_H_IC_2.text())
        except:
            if self.le_Sxeq_EC_2.text() == '' or self.le_Sxeq_IC_2.text() == '':
                self.warning_wdj('Choose a left and right cell first.')
            
            else:    
                self.warning_wdj('Corrupted cell. Check carefully cell database.')
            
            ok = 1

        return ok

# get geometric parameters --> read geometric parameters
    def get_geom_3(self):  
        ok = 0 
        try: 
                self.CAV_ge_2[0,0] = float(self.le_Sxeq_EC_2.text())            
                self.CAV_ge_2[0,1] = float(self.le_Syeq_EC_2.text())                 
                self.CAV_ge_2[0,2] = float(self.le_Sxir_EC_2.text())                 
                self.CAV_ge_2[0,3] = float(self.le_Syir_EC_2.text())                   
                self.CAV_ge_2[0,4] = float(self.le_ER_EC_2.text())  
                self.CAV_ge_2[0,5] = float(self.le_IR_EC_2.text())                       
                self.CAV_ge_2[0,6] = float(self.le_SL_EC_2.text())
                
                self.CAV_ge_2[2,0] = float(self.le_Sxeq_IC_2.text())            
                self.CAV_ge_2[2,1] = float(self.le_Syeq_IC_2.text())                 
                self.CAV_ge_2[2,2] = float(self.le_Sxir_IC_2.text())                 
                self.CAV_ge_2[2,3] = float(self.le_Syir_IC_2.text())                   
                self.CAV_ge_2[2,4] = float(self.le_ER_IC_2.text())  
                self.CAV_ge_2[2,5] = float(self.le_IR_IC_2.text())                       
                self.CAV_ge_2[2,6] = float(self.le_SL_IC_2.text())
                              
        except:
            if self.le_Sxeq_EC_2.text() == '' or self.le_Sxeq_IC_2.text() == '':
                self.warning_wdj('Choose a left and right cell first.')
            else:   
                self.warning_wdj('Corrupted cell. Check carefully cell database.')
            ok = 1

        return ok

    # geometric to physic parameters convertion
    def g2p_3(self, CAV_ge, n): 
        CAV = np.zeros((7))
        CAV[0] = CAV_ge[0]
        CAV[1] = CAV_ge[1]
        CAV[2] = CAV_ge[2]
        CAV[3] = CAV_ge[3]
        CAV[4] = CAV_ge[4]
        CAV[5] = CAV_ge[5]
        CAV[6] = CAV_ge[6]
        
        geom=Geometry()
        XYP = geom.racc_point(CAV)
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
  
        if n == 0:          
            self.le_IRpy_EC_2.setText(str(round(R_ir,self.round_val)))
            self.le_alpha_EC_2.setText(str(round(alpha,self.round_val)))
            self.le_R_EC_2.setText(str(round(R,self.round_val)))
            self.le_r_EC_2.setText(str(round(r,self.round_val)))
            self.le_d_EC_2.setText(str(round(d,self.round_val)))
            self.le_SLpy_EC_2.setText(str(round(L,self.round_val)))
            self.le_H_EC_2.setText(str(round(H,self.round_val)))
            
            self.CAV_py_2[0,:] = np.array([R_ir,alpha,R,r,d,L,H]) 
        
        elif n == 1:          
            self.le_IRpy_IC_2.setText(str(round(R_ir,self.round_val)))
            self.le_alpha_IC_2.setText(str(round(alpha,self.round_val)))
            self.le_R_IC_2.setText(str(round(R,self.round_val)))
            self.le_r_IC_2.setText(str(round(r,self.round_val)))
            self.le_d_IC_2.setText(str(round(d,self.round_val)))
            self.le_SLpy_IC_2.setText(str(round(L,self.round_val)))
            self.le_H_IC_2.setText(str(round(H,self.round_val)))
            
            self.CAV_py_2[2,:] = np.array([R_ir,alpha,R,r,d,L,H]) 

    # physic to geometric parameters convertion
    def p2g_3(self, CAV_py, n):
        #try:
        R_ir = CAV_py[0]
        alpha = CAV_py[1]*np.pi/180
        R = CAV_py[2]
        r = CAV_py[3]
        d = CAV_py[4]
        L = CAV_py[5]
        H = CAV_py[6]
            
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
        
        if n == 0:
            self.le_Sxeq_EC_2.setText(str(round(A,self.round_val)))
            self.le_Syeq_EC_2.setText(str(round(B,self.round_val)))
            self.le_Sxir_EC_2.setText(str(round(a,self.round_val)))
            self.le_Syir_EC_2.setText(str(round(b,self.round_val)))
            self.le_ER_EC_2.setText(str(round(R_eq,self.round_val)))
            self.le_IR_EC_2.setText(str(round(R_ir,self.round_val)))
            self.le_SL_EC_2.setText(str(round(L,self.round_val)))
        
            self.CAV_ge_2[0,:] = np.array([A,B,a,b,R_eq,R_ir,L])
        
        elif n == 1:
            self.le_Sxeq_IC_2.setText(str(round(A,self.round_val)))
            self.le_Syeq_IC_2.setText(str(round(B,self.round_val)))
            self.le_Sxir_IC_2.setText(str(round(a,self.round_val)))
            self.le_Syir_IC_2.setText(str(round(b,self.round_val)))
            self.le_ER_IC_2.setText(str(round(R_eq,self.round_val)))
            self.le_IR_IC_2.setText(str(round(R_ir,self.round_val)))
            self.le_SL_IC_2.setText(str(round(L,self.round_val)))
        
            self.CAV_ge_2[2,:] = np.array([A,B,a,b,R_eq,R_ir,L])

##########################################################################################################
    # Database single cell
    def Database_sc(self):
        widget_IC = CellDb(self, self.row1, self.row2)
        widget_IC.exec_()
        try:
            self.pathDB=widget_IC.button_cancel()
        except:        
            self.pathDB=widget_IC.button_ok()    

##########################################################################################################
    # Run elmg simulation
    def button_run_elmg_simulation_3(self):
        F_target=0
        emfn1=emfn()
        
        self.define_elmg_path('function')
        ok = 0
        try:
            F_target = float(self.le_f_3.text())
            if F_target < 0:
                self.warning_wdj('Frequency target must be positive float number!')
                ok = 1
        except:
            self.warning_wdj('Frequency target must be positive float number!')
            ok = 1   

        if ok == 0 and self.path_to_elmg_file != '':
            CAV = np.zeros((3,8))

            if self.cb_geometric_3.isChecked() == True and self.get_geom_3() == 0:
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]:
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.le_ER_IC_2.setText(str(self.CAV_ge_2[0,4]))
                        ok = 0
                    else:
                        ok = 1
                
            elif self.cb_physic_3.isChecked() == True and self.get_phisic_3() == 0:
                self.p2g_3(self.CAV_py_2[0,:], 0)
                self.p2g_3(self.CAV_py_2[2,:], 1)
                CAV[0,0:7] = self.CAV_ge_2[0,0:7]
                CAV[2,0:7] = self.CAV_ge_2[2,0:7]
                CAV[0,7] = 19
                if CAV[0,4] != CAV[2,4]: 
                    if self.uniform_equator_diameter() == 'yes':
                        CAV[2,4] = CAV[0,4]
                        self.CAV_ge_2[2,4] = self.CAV_ge_2[0,4]
                        self.g2p_3(self.CAV_ge_2[2,:], 1)
                        ok = 0
                    else:
                        ok = 1   
                        
        if self.path_to_elmg_file != '':
            if ok == 0 and self.get_tube_lenght(CAV) == 0:  
                CAV[1,-1] = float(self.le_tube_length_2.text())
                CAV[2,-1] = float(self.le_tube_length_Rir_2.text())        
            else: 
                ok = 1
                
            if ok == 0:  
                dx = CAV[0,2]/5
                self.beta=emfn1.def_beta_EG(F_target, CAV)
                self.le_beta_3.setText(str(self.beta))
            
            if F_target>0:
                try:
                    elmg_sim=self.button_run_elmg_simulation2_2(self.path_to_elmg_file, CAV, ok, F_target, dx) #### ????
                except Exception as E:
                    print(E)

                if path.exists(self.path_to_elmg_file+'\\elmg_file\\temp.txt'):   
                    try:
                        temp=open(self.path_to_elmg_file+'\\elmg_file\\temp.txt', 'r')
                        cont=temp.readlines()
                        freq=(cont[0].split(','))[0]
                        self.le_f_3.setText(freq)
                        self.le_beta_3.setText((cont[0].split(','))[1])
                        temp.close()
                        self.frame_sf_execution_3.show()
                        
                        self.lb_se_f_3.setText('Frequency [' + (cont[1].split(','))[1] + '] = ' + (cont[1].split(','))[0])            
                        self.lb_se_q_3.setText('Q BCS factor @ 2K = ' + (cont[1].split(','))[2])
                        self.lb_se_rq_3.setText('r/Q [' + (cont[1].split(','))[4] + '] = ' + (cont[1].split(','))[3]) 
                        self.lb_se_E_3.setText('Epeak/Eacc =' + (cont[1].split(','))[5])
                        self.lb_se_H_3.setText('Hpeak/Eacc [mT/(MV/m)] = ' + (cont[1].split(','))[6]) 
                        self.lb_se_K_3.setText('K [coupling, %] = ' + (cont[1].split(','))[7]) 
                        
                        self.tempArray[0,0]=float((cont[1].split(','))[0]) # freq
                        self.tempArray[0,1]=float((cont[1].split(','))[2]) # qbcs
                        self.tempArray[0,2]=float((cont[1].split(','))[3]) # r/q
                        self.tempArray[0,3]=float((cont[1].split(','))[5]) # e/eacc
                        self.tempArray[0,4]=float((cont[1].split(','))[6]) # h/eacc
                        self.tempArray[0,5]=float((cont[1].split(','))[7]) # k
                    except:
                        self.warning_wdj('Something went wrong')
                    remove(self.path_to_elmg_file+'\\elmg_file\\temp.txt')
                
                if path.exists(self.path_to_elmg_file+'\\elmg_file\\temp_tune.txt'):
                    CAV=self.CAV_tuning
                    self.fill_g_param_2(CAV) 

# draw single cell profile
    def draw_new_SC(self,IC_EG,l1,l2,CAV,path_to_elmg_file):
        try:
            x = Draw_cavity_profile('', IC_EG, 1)

            IC_coo = x.CAV_coo()
            IC_coo[:,0] = -IC_coo[:,0] + IC_coo[-1,0] 
            IC_coo[:,0] = np.flip(IC_coo[:,0])
            IC_coo[:,1] = np.flip(IC_coo[:,1])

            self.EC_EG = np.zeros((3,8))
            self.EC_EG[0,:] = CAV[0,:]
            self.EC_EG[0,7] = 16
            x = Draw_cavity_profile('', self.EC_EG, 1)
            EC_coo = x.CAV_coo()
            EC_coo[:,0] = EC_coo[:,0] + IC_coo[-1,0]
        
            CAV_coo = np.append(IC_coo, EC_coo, axis = 0)
            end = CAV_coo[-1,0]
            
            if l2 == 0:
                add = np.array([[end + l1, CAV_coo[-1,1]],
                                [end + l1, 0],
                                [0,0]])
                                #[CAV_coo[0,0], CAV_coo[0,1]]])
                                #[CAV_coo[0,0], CAV_coo[0,1]]])
            else:
                add = np.array([[end + l2, CAV_coo[-1,1]],
                                [end + l2 + np.abs(CAV[0,5]-CAV[2,5]), CAV_coo[0,1]],
                                [end + l1, CAV_coo[0,1]],
                                [end + l1, 0],
                                [0,0],
                                [CAV_coo[0,0], CAV_coo[0,1]]])
            CAV_coo = np.append(CAV_coo, add, axis = 0)
            CAV_coo2=[]
            CAV_coo2.append(CAV_coo[0,:])
            CAV_coo[:,0]=CAV_coo[:,0]+float(l2)
            CAV_coo2.append(CAV_coo)

            temp_coo=np.array([[CAV_coo[0,0], CAV_coo[0,1]]])
            CAV_coo[:,0]+=l1
            temp_coo=np.append(temp_coo, CAV_coo, axis=0)
            temp2=np.array([[0,0], 
                            [temp_coo[0,0], temp_coo[0,1]]])
            temp_coo=np.append(temp_coo, temp2, axis=0)
            ax=self.figure.add_subplot(1,1,1)     
            ax.plot(temp_coo[:,0], temp_coo[:,1], 'r-')
            self.canvas.draw()

            l=''
            file=open(path_to_elmg_file+"\\fileDraw.txt",'w')
            for i in range(len(temp_coo)):
                l+=str(temp_coo[i,0])+','+str(temp_coo[i,1])+'\n'
            file.write(l)
            file.close()
            plt.savefig(path_to_elmg_file+"\\fileDraw.png")
        except:
            self.warning_wdj('Something wrong during the cavity profile definition')

#######################################################################################
#### Re-entrant cavity

##############################################################################            
# reset all the parameters values            
    def reset_param_tab2(self):
        self.le_f_4.setText('')
        self.le_bt_r.setText('')
        self.le_bt_l.setText('')
        self.le_l.setText('')
        self.le_m.setText('')
        self.le_u.setText('')
        self.le_gap.setText('')
        self.le_sh.setText('')
        self.le_l_m.setText('')
        self.le_angle.setText('')
        self.le_path.setText('')
        self.le_beta_4.setText('')
        self.figure.clf()
        self.canvas.draw()

##############################################################################
# read the parameters values
    def read_param(self):
        if self.le_f_4.text()=='':
            self.frequency=0
        else:
            self.frequency=float(self.le_f_4.text()) #MHz
        
        if self.le_bt_r.text()=='':
            self.bt_radius=0
        else:
            self.bt_radius=float(self.le_bt_r.text())
        
        if self.le_bt_l.text()=='':
            self.bt_length=0
        else:
            self.bt_length=float(self.le_bt_l.text())
            
        if self.le_l.text()=='':
            self.l_radius=0
        else:
            self.l_radius=float(self.le_l.text())
        
        if self.le_m.text()=='':
            self.m_radius=0
        else:
            self.m_radius=float(self.le_m.text())

        if self.le_u.text()=='':
            self.u_radius=0
        else:
            self.u_radius=float(self.le_u.text())
            
        if self.le_gap.text()=='':
            self.gap=0
        else:
            self.gap=float(self.le_gap.text())
            
        if self.le_sh.text()=='':
            self.sh=0
        else:
            self.sh=float(self.le_sh.text())
        
        if self.le_l_m.text()=='':
            self.l_m=0
        else:
            self.l_m=float(self.le_l_m.text())
        
        if self.le_angle.text()=='':
            self.b_angle=0
        else:
            self.b_angle=float(self.le_angle.text())
            
        if self.le_beta_4.text()=='':
            self.beta=0
        else:
            self.beta=float(self.le_beta_4.text())        

##############################################################################

    #### DESIGN OF BEAM TUBE
    def tube_design(self):
        self.read_param()
        l1_start_x = 0
        l1_start_y = 0
        l1_stop_x = 0
        l1_stop_y = self.bt_radius

        l2_start_x = l1_stop_x
        l2_start_y = l1_stop_y
        l2_stop_x = l2_start_x + self.bt_length
        l2_stop_y = l2_start_y
        return l2_start_x, l2_start_y, l2_stop_x, l2_stop_y
    
##############################################################################

    #### DESIGN OF LOWER BLEND
    #Here, we need to find the parameter of the line going from lower to medium circles that needs to be tangent to the lower circle and having b_angle
    # Initial parameters for circle
    def lower_blend(self):
        self.read_param()
        l_center_x = self.tube_design()[2]
        l_center_y = self.tube_design()[3] + self.l_radius
        l_start_x = self.tube_design()[2]
        l_start_y = self.tube_design()[3]
        #print('center of first circle: x0='+str(l_center_x)+'y0='+str(l_center_y))
        self.l_center_x=float(l_center_x)
        self.l_center_y=float(l_center_y)
        return l_center_x, l_center_y
    
    ##############################################################################

    #### LINE TANGENT TO LOWER CIRCLE
    def line_tang_1(self):    
        self.read_param()
        x, y, x0, y0, m, b, R = sm.symbols('x y x0 y0 m b R')
        circle = (x-x0)**2+(y-y0)**2-R**2
        line = y-m*x-b
        # Substitute line into circle
        circle_red = circle.subs(y, m*x+b)
        # Solve new equation
        sol = sm.solve(circle_red, x)
        # If the line is tangent, the discriminat in null and we can calculate b
        discr = R**2*m**2 + R**2 - b**2 - 2*b*m*x0 + 2*b*y0 - m**2*x0**2 + 2*m*x0*y0 - y0**2
        b_tg = sm.solve(discr, b)[1]
        ##print(b_tg)
        l3_m = np.tan(-self.b_angle)
        
        l_center_x=self.lower_blend()[0]
        l_center_y=self.lower_blend()[1]
        l3_b = float(b_tg.subs({R:self.l_radius, m:l3_m, x0:l_center_x, y0:l_center_y}))
        ##print('Line tangent to lower circle. m = {:.2f} b = {:.2f}'.format(l3_m, l3_b))
        # if the discriminat is null, the l_stself.op_x is easily done by
        l_stop_x = (-l3_b*l3_m+l3_m*l_center_y+l_center_x)/(l3_m**2+1)
        # and consequently the y position is calculated
        l_stop_y = np.sqrt(self.l_radius**2-(l_stop_x-l_center_x)**2)+l_center_y
        ##print('Point of tangent of l circle to line: x = {:.4f}, y = {:.4f}'.format(l_stop_x, l_stop_y))
        self.l_stop_x=l_stop_x
        self.l_stop_y=l_stop_y
        self.dx1=float(l_stop_x)-self.l_center_x
        self.dy1=float(l_stop_y)-self.l_center_y
        return discr,l3_m,l3_b,l_stop_x,l_stop_y,circle
    
    ##############################################################################

    #### POSITIONING OF MIDDLE CIRCLE TO BE TANGENT TO LINE COMING FROM LOWER CIRCLE
    # The circle center in x is positioned based on the geometry. The circle center in y is positioned based to be tangent to the line coming from the lower circle.
    def circles(self):
        self.read_param()
        m_center_x = self.bt_length+self.l_radius+self.gap-self.u_radius+self.m_radius
        # The discriminat calculated before needs to be zero for tangency and this allows calculating y0. We take the solution with positive y (we want the circle to be above the line)
        x, y, x0, y0, m, b, R = sm.symbols('x y x0 y0 m b R')
        discr=self.line_tang_1()[0]
        y0_tg = sm.solve(discr, y0)[1]
        ##print(y0_tg)
        l3_m=self.line_tang_1()[1]
        l3_b=self.line_tang_1()[2]
        m_center_y = float(y0_tg.subs({R:self.m_radius, m:l3_m, b:l3_b, x0:m_center_x}))
        ##print('Center medium circle: x = {:.4f}, y = {:.4f}'.format(m_center_x, m_center_y))
        self.m_center_x=m_center_x
        self.m_center_y=m_center_y
        # Beign the discriminat null for tangency, x is given by
        m_start_x = (-l3_b*l3_m+l3_m*m_center_y+m_center_x)/(l3_m**2+1)
        m_start_y = -np.sqrt(self.m_radius**2-(m_start_x-m_center_x)**2)+m_center_y
        self.m_start_x=m_start_x
        self.m_start_y=m_start_y
        #print('Start point medium circle: x = {:.4f}, y = {:.4f}'.format(m_start_x, m_start_y))

        #### THE END POINT OF MIDDLE CIRCLE IS AT X=R AND Y=0 W.R.T. CIRCLE CENTER
        m_stop_x = m_center_x-self.m_radius
        m_stop_y = m_center_y
        self.dx2=float(m_stop_x)-self.m_center_x
        self.dy2=float(m_stop_y)-self.m_center_y
        self.m_stop_x=m_stop_x
        self.m_stop_y=m_stop_y
        ##print('Stop point medium circle: x = {:.4f}, y = {:.4f}'.format(m_stop_x, m_stop_y))

        #### THE VERTICAL LINE WILL END SFH
        l_end_x = m_stop_x
        l_end_y = m_stop_y +self.sh
        self.l_end_x=l_end_x
        self.l_end_y=l_end_y
        ##print('End point line: x = {:.4f}, y = {:.4f}'.format(l_end_x, l_end_y))

        #### DEFINE UPPER CIRCLE
        u_center_x = l_end_x + self.u_radius
        u_center_y = l_end_y
        self.u_center_x=u_center_x
        self.u_center_y=u_center_y
        ##print('Center upper circle: x = {:.4f}, y = {:.4f}'.format(u_center_x, u_center_y))

        x1, y1, R1 = sm.symbols('x1 y1 R1')
        circle1 = sm.Eq((x-x1)**2+(y-y1)**2-R1**2,0)
        
        circle=self.line_tang_1()[5]
        sol = sm.solve([circle, circle1], [x,y])[1][0]
        m_stop_x = float(sol.subs({R:self.m_radius, x0:m_center_x, y0:m_center_y, R1:self.u_radius, x1:u_center_x, y1:u_center_y}))
        ##print(m_stop_x, np.sqrt(m_radius**2-(m_stop_x-m_center_x)**2)+m_center_y)
        ##print(m_stop_x, np.sqrt(u_radius**2-(m_stop_x-u_center_x)**2)+u_center_y)
        ##print(sol)

        dx0, dy0 = sm.symbols('dx0 dy0')
        sol1 = sol.collect(y0, evaluate=True).collect(y1, evaluate=True).subs(x0**2-2*x0*x1+x1**2, (x0-x1)**2, evaluate=True).subs(y0**2-2*y0*y1+y1**2, (y0-y1)**2, evaluate=True).subs(-R**2+2*R*R1-R1**2, -(R-R1)**2, evaluate=True).subs(R**2+2*R*R1+R1**2, (R+R1)**2, evaluate=True).subs(x0-x1, dx0).subs(y0-y1, dy0)
        ##print(sol1)
        m_stop_x = float(sol1.subs({R:self.m_radius, x0:m_center_x, y0:m_center_y, R1:self.u_radius, x1:u_center_x, y1:u_center_y, dx0:m_center_x-u_center_x, dy0:m_center_y-u_center_y}))
        ##print(m_stop_x, np.sqrt(m_radius**2-(m_stop_x-m_center_x)**2)+m_center_y)
        return m_center_x,m_center_y, m_start_x,m_start_y, m_stop_x,m_stop_y, l_end_x,l_end_y, u_center_x,u_center_y
    
    # Run SuperFish
    def param_computation(self):

        if self.name_project.text()=='':
            self.warning_wdj("Please define a new project or open an existing one.")
        else:

            self.read_param()
            if self.frequency==0 or self.bt_radius==0 or self.bt_length==0 or self.l_radius==0 or self.m_radius==0 or self.u_radius==0 or self.gap==0 or self.sh==0 or self.l_m==0 or self.b_angle==0:
                self.warning_wdj("Please fill all the parameters.")
            else:
                self.circles()
                zctr=self.u_center_x/10
                clength=self.u_center_x/10+self.u_radius/10-self.m_stop_x/10-1
                testo=['Simulation for frequency guess\n \n',
                '$reg kprob=1,\n',
                'dx=0.10 , freq='+str(self.frequency)+' \n',
                'xdri='+str(zctr)+', ydri='+str(self.u_center_y/10+self.u_radius/10-0.5)+'\n',
                'nbslf=1, nbsrt=1, \n',
                'beta='+str(self.beta)+', rmass = -1, kmethod=1, \n', 
                'irtype=0 ',
                'zctr='+str(zctr)+', clength='+str(clength)+' norm=1 EZEROT=1.4e6$ \n \n'
                ]
        
                testo+=['$po x=0.0, y=0.0$ \n',
                        '$po x=0, y='+str(self.bt_radius/10)+'$ \n',
                        '$po x='+str(self.bt_length/10)+', y='+str(self.bt_radius/10)+'$ \n',
                        '$po NT=2, x0='+str(self.l_center_x/10)+', y0='+str(self.l_center_y/10)+', A='+str(self.l_radius/10)+', B='+str(self.l_radius/10)+', x='+str(self.dx1/10)+', y='+str(self.dy1/10)+'$ \n',
                        '$po x='+str(self.m_start_x/10)+', y='+str(self.m_start_y/10)+'$ \n',
                        '$po NT=2, x0='+str(self.m_center_x/10)+', y0='+str(self.m_center_y/10)+', A='+str(self.m_radius/10)+', B='+str(self.m_radius/10)+', x='+str(self.dx2/10)+', y='+str(self.dy2/10)+'$ \n',
                        '$po x='+str(self.l_end_x/10)+', y='+str(self.l_end_y/10)+'$ \n',
                        '$po NT=2, x0='+str(self.u_center_x/10)+', y0='+str(self.u_center_y/10)+', A='+str(self.u_radius/10)+', B='+str(self.u_radius/10)+', x='+str(0)+', y='+str(self.u_radius/10)+'$ \n',
                        '$po NT=2, x0='+str(self.u_center_x/10)+', y0='+str(self.u_center_y/10)+', A='+str(self.u_radius/10)+', B='+str(self.u_radius/10)+', x='+str(self.u_radius/10)+', y='+str(0)+'$ \n',
                        '$po x='+str(self.u_center_x/10+self.u_radius/10)+', y='+str(self.u_center_y/10-(self.l_end_y/10-self.m_stop_y/10))+'$ \n'
                        '$po NT=2, x0='+str(self.u_center_x/10+self.u_radius/10-self.m_radius/10)+', y0='+str(self.m_center_y/10)+', A='+str(self.m_radius/10)+', B='+str(self.m_radius/10)+', x='+str(self.m_center_x/10-self.m_start_x/10)+', y='+str(-self.m_center_y/10+self.m_start_y/10)+'$ \n',
                        '$po x='+str(self.u_center_x/10+self.u_radius/10-self.m_radius/10+self.m_center_x/10-self.m_start_x/10-(self.l_stop_x/10-self.m_start_x/10))+', y='+str(self.m_center_y/10-self.m_center_y/10+self.m_start_y/10+(self.l_stop_y/10-self.m_start_y/10))+'$ \n',
                        '$po NT=2, x0='+str(self.u_center_x/10+self.u_radius/10-self.m_radius/10+self.m_center_x/10-self.m_start_x/10-(self.l_stop_x/10-self.m_start_x/10)+self.dx1/10)+', y0='+str(self.m_center_y/10-self.m_center_y/10+self.m_start_y/10+(self.l_stop_y/10-self.m_start_y/10)-self.dy1/10)+', A='+str(self.l_radius/10)+', B='+str(self.l_radius/10)+', x='+str(0)+', y='+str(-self.l_radius/10)+'$ \n',
                        '$po x='+str(self.u_center_x/10+self.u_radius/10-self.m_radius/10+self.m_center_x/10-self.m_start_x/10-(self.l_stop_x/10-self.m_start_x/10)+self.dx1/10+self.bt_length/10)+', y='+str(self.m_center_y/10-self.m_center_y/10+self.m_start_y/10+(self.l_stop_y/10-self.m_start_y/10)-self.dy1/10-self.l_radius/10)+'$ \n',
                        '$po x='+str(self.u_center_x/10+self.u_radius/10-self.m_radius/10+self.m_center_x/10-self.m_start_x/10-(self.l_stop_x/10-self.m_start_x/10)+self.dx1/10+self.bt_length/10)+' y='+str(0)+'$ \n',
                        '$po x=0, y=0$']

                self.define_elmg_path('function')
                #folder = getcwd()+"\\runs" # old
                folder = self.path_to_elmg_file
                #print('folder=',folder)
                #folder="C:\\Users\edelcore\Documents\BriXSinO\hb2tf\\buncher\Superfish\Elisa\provaPython"
                new_folder=str(self.frequency)
                path=os.path.join(folder,new_folder)
                try:
                    os.makedirs(path, exist_ok = True)
                except OSError as error:
                    self.warning_wdj("Directory '%s' can not be created")
                #mkdir(join(folder,new_folder))
                file_name1='prova_@'+str(int(self.frequency))
                file_name='prova_@'+str(int(self.frequency))+'.af'
                path_superfish=os.path.join(path,file_name)
                        
                file  = open(path_superfish, 'w')
                file.write(''.join(testo))
                file.close()
                scall(path_superfish, shell=True)
        
                #### write SGF
                sfo_file  = open(path+'\\'+file_name1+'.SFO', 'r')
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
                    
                sgf_file =  open(path+'\\'+file_name1+'.SGF', 'w')
                lines = ['; SEGFIELD control file',
                'OUTPUT_file '+file_name1+'',
                'INPUT_filename '+file_name1+'.SFO',
                ' ',
                'SEGment_numbers      2 to ' + str(segments[-1]),
                ';E0T' + str(1E6),
                'NodesOnly',
                'ENDFILE']
                sgf_file.write('\n'.join(lines))
                sgf_file.close()
                scall(path+'\\'+file_name1+'.SGF', shell=True)
        
                
                tbl_file  = open(os.path.join(folder,new_folder)+'\\'+file_name1+'.TBL', 'r')
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
                
                fd_file  = open(path + '\\field_data.txt', 'w')
                fd_file.writelines(cont[n_begin : n_end])
                fd_file.close()
                
                if unit_press == 'kPa':
                    DAT = np.loadtxt(path + '\\field_data.txt')
                    DAT[:,6] *= 10**3
                    np.savetxt(path + '\\field_data.txt', DAT)  
                
                self.path=path
                #self.frame.show()
                #self.le_path.setText(path)

                self.draw_cav_tab2()
####
#### Draw Re-entrant cavity profile
    def draw_cav_tab2(self):
        try:
            fd_file  = np.genfromtxt(path.join(self.path,'field_data.txt'), usecols=(0,1))
            self.figure_2.clf()
            ax=self.figure_2.add_subplot(1,1,1)        
            ax.plot(fd_file[:,0], fd_file[:,1], 'r-') 
            ax.axis('equal')
            ax.axis('off')
            self.canvas_2.draw()
        except:
            self.warning_wdj('Run before!!')

####
# Open database
    def open_cav_database_2(self):
        if self.name_project.text()=='':
            self.warning_wdj('Please define a new project or open an existing one.')
        else:
            widget_2 = buncher_db(self)
            widget_2.exec_()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuildCav2()
    window.show()
    sys.exit(app.exec_())

###########################################################################

# ------> CAV
# [0,:] = EC
# [1,:] = PC
# [2,:] = IC
        
# [0,0] X semiaxis for equator ellipse
# [0,1] Y semiaxis for eqator ellipse
# [0,2] X semiaxis for iris ellipse
# [0,3] Y semiaxis for iris ellipse  
# [0,4] equatorial radius
# [0,5] iridal radius
# [0,6] semicell lenght   
    
# [0,1:15] = numero celle
# [0,16] = end cell
# [0,17] = pen cell
# [0,18] = inner cell
# [0,19] = terminal group
# [0,20] = terminal dumbell
# [0,21] = inner dumbell   
    
# [1,-1] = beam tube length (left)    
# [2,-1] = beam tube length (right)  
    
# ------> elmg_param   
# 0 Eacc
# 1 dx
# 2 temp_type (1-->RT    2-->cold)
# 3 beta_type (1-->geom    2-->opt)  
# 4 part_acc (1-->proton    2-->electron) 
# 5 res_freq 
# 6 res_freq_um 
# 7 TTf 
# 8 stored_energy 
# 9 stored_energy_um                      
# 10 P_diss 
# 11 P_diss_um 
# 12 R_s
# 13 R_s_um 
# 14 Q_factor
# 15 Shunt
# 16 Shunt_um
# 17 rQ
# 18 rQ_um 
# 19 RsQ 
# 20 RsQ_um 
# 21 beta    
# 22 mode (-1-->0    -2-->pi   float-->f_guess) 
# 23 overmetal 1
# 24 overmetal 2    