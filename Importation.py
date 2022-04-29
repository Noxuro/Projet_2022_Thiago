# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:27:02 2022

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
                             QMainWindow,QRadioButton,QListWidget,QComboBox)

ViewA=None

hostname = "192.168.1.78"#Maison
#hostname = "10.10.96.228"#ecole
username = "etudiant"
password = "vitrygtr"
port = 22


from Creation import View_C

class View_I(QWidget):
    
    def __init__(self, ViewA):
        super().__init__()
        
        self.viewA=ViewA
        self.setWindowIcon(QIcon('healer.jpeg'))
        
        self.B_view=QPushButton('View')
        self.B_take=QPushButton('Take it!',clicked = lambda : self.take(self.viewA))
        self.liste=QComboBox()
        self.B_return=QPushButton('Retour')
        self.Bcrea=QPushButton('Créé-en un !',clicked = lambda : self.creation(self.viewA))
        
        self.init_ui()
        
        self.show()
        
    def init_ui(self):
        
        H_box=QHBoxLayout()
        
        H_box.addWidget(self.B_view)
        H_box.addWidget(self.B_take)
        
        B_box=QHBoxLayout()
        
        B_box.addWidget(self.B_return)
        B_box.addWidget(self.Bcrea)
        
        G_box=QVBoxLayout()
        
        G_box.addLayout(H_box)
        G_box.addWidget(self.liste)
        G_box.addLayout(B_box)
        
        self.setLayout(G_box)
        self.setWindowTitle('Importation')
        
        self.B_return.clicked.connect(self.retour)
        self.B_view.clicked.connect(self.montrerV)
        
    def retour(self):
        self.hide()
        self.viewA.show()
        
    def take(self,viewA):
        self.file=self.liste.currentText()
        
        #print(self.file)
        self.file=self.file.split('_')
        self.file.pop()
        #print(self.file)
        self.nom=self.file[0]
        self.prenom=self.file[1]
        self.age=self.file[2]
        self.sexe=self.file[3]
        print(self.sexe)
        
        self.hide()
        self.viewC= View_C(viewA,self.nom,self.prenom,self.age,self.sexe)
    
    def creation(self,viewA):
        self.hide()
        self.viewC= View_C(viewA)
    
    def montrerV(self):
        self.liste.clear()
        user=ssh(hostname,port,username,password)
        Liste=user.sendCommand()
        
        for i in Liste:
            self.liste.addItem(i)
            

class ssh:
    client = None
    
    def __init__(self, hostname, port, username, password):
        try:
            print("Connecting to server.")
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username, 
                                password=password)
            
            self.liste=[]
        except:
            print("Exception raised!")

    def sendCommand(self):
        if(self.client):
            
            stdin, stdout, stderr = self.client.exec_command("ls")
            #print (stdout.read().decode())
            self.liste=stdout.read().decode()
            
            
            
        else:
            print("Connection not opened.")
        Tuple=self.liste.split('\n')
        
        #print(Tuple)
        Tuple.pop()
        #print(Tuple)
        
        self.client.close()
        return Tuple
        
        

print(__name__)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hostname = "192.168.1.78"#Maison
    #hostname = "10.10.96.228"#Ecole
    username = "etudiant"
    password = "vitrygtr"
    port = 22
    
    viewI = View_I(ViewA)
    sys.exit(app.exec_())