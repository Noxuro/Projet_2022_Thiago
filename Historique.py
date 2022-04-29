# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:27:14 2022

@author: Theo
"""

import sys
import os
from paramiko import client
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import (QIntValidator,QPixmap,QIcon,QFont)
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QWidget, QLabel,QTextEdit,
                             QMainWindow,QRadioButton,QListWidget, QToolTip)

hostname = "192.168.1.78"#Maison
#hostname = "10.10.96.228"#ecole
username = "etudiant"
password = "vitrygtr"
port = 22

ViewC=None
ViewA=None
SCP=None

class View_H(QWidget):
    
    def __init__(self, ViewA,SCP,N="",P="",A="",S=""):
        super().__init__()
        
        self.viewA=ViewA
        self.SCP=SCP
        self.setWindowIcon(QIcon('healer.jpeg'))
        
        self.F_local=N+"_"+P+"_"+A+"_"+S+"_.txt"
        print(self.F_local)
        self.F_VM="/home/etudiant/"+self.F_local
        
        QToolTip.setFont(QFont('Arial', 14))
        self.setToolTip('')
        self.nom=''
        self.prenom=''
        
        
        self.Cnom=QLabel('Nom')
        self.Cprenom=QLabel('Prenom')
        self.Cage=QLabel('Age')
        
        self.Tnom=QLineEdit(N)
        self.Tprenom=QLineEdit(P)
        self.Tage=QLineEdit(A)
        
        self.Tnom.setFixedSize(150,20)
        self.Tprenom.setFixedSize(150,20)
        self.Tage.setFixedSize(150,20)
        
        self.Tnom.setAlignment(QtCore.Qt.AlignCenter)
        self.Tprenom.setAlignment(QtCore.Qt.AlignCenter)
        self.Tage.setAlignment(QtCore.Qt.AlignCenter)
        
        self.Tnom.setDisabled(True)
        self.Tprenom.setDisabled(True)
        self.Tage.setDisabled(True)
        
        self.Z_Prop=QTextEdit()
        
        self.B_return=QPushButton('Retour')
        
        self.init_ui()
        
        #récuperation donnée
        
        self.Hist=""
        with open(self.F_local,'r') as H:
            for L in H:
                self.Hist+=L
        H.close()
        self.SCP.closing()
        self.Z_Prop.setText(self.Hist)
        
        self.show()
        
    def init_ui(self):
         ## HAUT
         HG_label_box=QVBoxLayout()
         
         HG_label_box.addWidget(self.Cnom)
         HG_label_box.addWidget(self.Cprenom)
         HG_label_box.addWidget(self.Cage)
         
         
         HD_T_box=QVBoxLayout()
         
         HD_T_box.addWidget(self.Tnom)
         HD_T_box.addWidget(self.Tprenom)
         HD_T_box.addWidget(self.Tage)
         
         H_box=QHBoxLayout()
         
         H_box.addLayout(HG_label_box)
         H_box.addLayout(HD_T_box)
         
         ## BAS
         
         B_box=QVBoxLayout()
         
         B_box.addWidget(self.Z_Prop)
         B_box.addWidget(self.B_return)
         
         # GLOBAL
         G_box=QVBoxLayout()
         
         G_box.addLayout(H_box)
         G_box.addLayout(B_box)
         
         self.setLayout(G_box)
         self.setWindowTitle("Création")
         self.Z_Prop.setDisabled(True)
         self.B_return.clicked.connect(self.retour)
         
    def retour(self):
        self.hide()
        self.viewA.show()     

class SCP:
    client = None

    # Initialize the SSH and SFTP connexion
    def __init__(self,F_local,hostname=hostname, port=port,
                 username=username, password=password):
        self.F_local=F_local
        self.F_VM="/home/etudiant/"+self.F_local
        try:
            print("Connecting to server.")
            # Connexion to the VM
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username,
                                password=password)
            # Open the sftp client
            self.sftp = self.client.open_sftp()
            # Get the VM file
            self.get_file()
            # Creation of the local file if it doesn't exist
            open(F_local, 'a+').close()
        except:
            print("Exception raised in SSH!")
            raise Exception("La connexion à la VM a échoué")

    # Get and send all the values from the file
    def get_file(self):
        self.sftp.chdir("/home/etudiant/")
        try:
            self.sftp.stat(self.F_VM)
            self.sftp.get(self.F_VM,self.F_local)
        except IOError:
            print('file not exist')

    # Close the sftp and ssh connexion
    def closing(self):
        print(self.sftp.put(self.F_local,self.F_VM))
        self.client.close()
        
        
        
        
print(__name__)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    viewC = ViewC(ViewA)
    viewH = View_H(viewC)
    sys.exit(app.exec_())