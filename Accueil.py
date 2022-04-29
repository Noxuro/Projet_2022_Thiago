# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:25:27 2022

@author: Theo
"""

import sys
import os
from paramiko import client
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import (QIntValidator,QPixmap,QIcon)
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QWidget, QLabel,QTextEdit,
                             QMainWindow,QRadioButton,QListWidget)

from Creation import View_C
from Importation import View_I

class View_A(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.setWindowIcon(QIcon('healer.jpeg'))
        self.logo=QLabel()
        self.logo.setPixmap(QPixmap('healer.jpeg'))
        
        
        self.N=QLabel('Vous etes dans le registre des patients')
        self.Bvn=QLabel('Bienvenue!')
        
        self.Bcrea=QPushButton('Création',
                               clicked = lambda : self.creation(viewA))
        
        self.Bimport=QPushButton('Importation',
                                 clicked = lambda : self.importation(viewA))
        
        self.N.setAlignment(QtCore.Qt.AlignCenter)
        self.Bvn.setAlignment(QtCore.Qt.AlignCenter)
        
        
        self.init_ui()
        
        self.show()
        
    def init_ui(self):
        
        Global_box=QVBoxLayout()
        
        Global_box.addWidget(self.logo)
        Global_box.addWidget(self.N)
        Global_box.addWidget(self.Bvn)
        Global_box.addWidget(self.Bcrea)
        Global_box.addWidget(self.Bimport)
        
        self.setLayout(Global_box)
        self.setWindowTitle("Accueil")
        
    def creation(self,viewA):
        self.hide()
        self.viewC= View_C(viewA)
        
    def importation(self,viewA):
        self.hide()
        self.viewI= View_I(viewA)
        
        
        
        
        
        
print(__name__)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hostname = "192.168.1.78"
    username = "etudiant"
    password = "vitrygtr"
    port = 22
    viewA = View_A()
    sys.exit(app.exec_())