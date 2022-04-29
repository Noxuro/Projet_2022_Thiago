# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:25:49 2022

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

from Historique import View_H,SCP

hostname = "192.168.1.78"#Maison
#hostname = "10.10.96.228"#ecole
username = "etudiant"
password = "vitrygtr"
port = 22

ViewA=None


class View_C(QWidget):
    
    def __init__(self, ViewA,N="",P="",A='',S=''):
        super().__init__()
        
        self.viewA=ViewA

        self.setWindowIcon(QIcon('healer.jpeg'))
        
        self.F_local=N+"_"+P+"_"+A+"_"+S+"_.txt"
        self.F_VM="/home/etudiant/"+self.F_local
        
        QToolTip.setFont(QFont('Arial', 14))
        self.setToolTip('')
        self.nom=N
        self.prenom=P
        self.age=A
        self.sexe=S
        print(self.sexe)
        
        self.Cnom=QLabel('Nom')
        self.Cprenom=QLabel('Prenom')
        self.Cage=QLabel('Age')
        self.Csexe=QLabel('Sexe')
        
        self.Tnom=QLineEdit(self.nom)
        self.Tprenom=QLineEdit(self.prenom)
        self.Tage=QLineEdit(self.age)
        
        self.Tnom.setFixedSize(150,20)
        self.Tprenom.setFixedSize(150,20)
        self.Tage.setFixedSize(150,20)
        
        
        self.R_H=QRadioButton('Homme')
        self.R_F=QRadioButton('Femme')
        
        self.espace=QLabel()
        self.espace.setFixedSize(300,20)
        
        self.B_Hist=QPushButton('Historique',
                                clicked = lambda : self.historique(self.viewA))
        
        self.B_register=QPushButton('Enregistrement')
        self.B_return=QPushButton('Retour')
        
        self.B_return.setToolTip('Vous pouvez retourner à l\'accueil en appuyant ici')
        
        if self.nom=='':
            self.B_Hist.setToolTip("Veillez à remplir le formulaire avant de cliquer")
            self.B_register.setToolTip("Veillez à remplir le formulaire avant de cliquer")
            
        else:
            self.B_Hist.setToolTip('Cliquez pour accéder à l\'historique de '+
                                   self.nom+' '+self.prenom)
            self.B_register.setToolTip('Cliquez pour enregistrer le fichier de '+
                                   self.nom+' '+self.prenom)
        
        
        self.Tnom.textChanged.connect(self.P_register)
        self.Tprenom.textChanged.connect(self.P_register)
        self.Tage.textChanged.connect(self.P_register)
        
        self.C_DialS=QLabel('Symptôme : ')
        self.C_DialS.setAlignment(QtCore.Qt.AlignCenter)
        self.Z_DialS=QTextEdit()
        self.Z_DialS.textChanged.connect(self.Medocs)
        
        self.C_DialO=QLabel('Ordonnances : ')
        self.C_DialO.setAlignment(QtCore.Qt.AlignCenter)
        self.Z_DialO=QTextEdit()
        
        
        self.Z_Prop=QTextEdit()
        
        # MEDICAMENT
        self.repertoire={"Doliprane":['douleur','fievre','paracetamol','gelules'],
                         "Dafalgan":['douleur','fievre','paracetamol','effervescent'],
                         "Efferalgant":['douleur','fievre','paracetamol','effervescent'],
                         "Kardegic":["vasculaires","cérébraux","cardiaque"],
                         "Spasfon":["douleur","digestif","contraction"],
                         "Gaviscon":["brulures","estomac","indigestion"],
                         "Dexeryl":["irritation","cutanées"],
                         "Meteospasmyl":["digestifs","ballonement"],
                         "Biseptine":["lésion","cutanées","infectées","infection"],
                         "Eludril":["infecion","bouche"]}
        
        self.init_ui()
        
        self.show()
        
    def init_ui(self):
        ## HAUT-GAUCHE
        HG_label_box=QVBoxLayout()
        
        HG_label_box.addWidget(self.Cnom)
        HG_label_box.addWidget(self.Cprenom)
        HG_label_box.addWidget(self.Cage)
        HG_label_box.addWidget(self.Csexe)
        
        HG_radio_box=QHBoxLayout()
        
        HG_radio_box.addWidget(self.R_H)
        HG_radio_box.addWidget(self.R_F)
        
        HG_T_R_box=QVBoxLayout()
        
        HG_T_R_box.addWidget(self.Tnom)
        HG_T_R_box.addWidget(self.Tprenom)
        HG_T_R_box.addWidget(self.Tage)
        HG_T_R_box.addLayout(HG_radio_box)
        
        HG_box=QHBoxLayout()
        
        HG_box.addLayout(HG_label_box)
        HG_box.addLayout(HG_T_R_box)
        
        ## HAUT-DROITE
        HD_box=QHBoxLayout()
        
        HD_box.addWidget(self.espace)
        HD_box.addWidget(self.B_Hist)
        
        ## HAUT
        H_box=QHBoxLayout()
        H_box.addLayout(HG_box)
        H_box.addLayout(HD_box)
        
        ## BAS-GAUCHE
        
        BG_box=QVBoxLayout()
        
        BG_box.addWidget(self.C_DialS)
        BG_box.addWidget(self.Z_DialS)
        BG_box.addWidget(self.C_DialO)
        BG_box.addWidget(self.Z_DialO)
        BG_box.addWidget(self.B_register)
        
        ## BAS-DROITE
        
        BD_box=QVBoxLayout()
        
        BD_box.addWidget(self.Z_Prop)
        BD_box.addWidget(self.B_return)
        
        ## BAS
        B_box=QHBoxLayout()
        B_box.addLayout(BG_box)
        B_box.addLayout(BD_box)
        
        # GLOBAL
        G_box=QVBoxLayout()
        
        G_box.addLayout(H_box)
        G_box.addLayout(B_box)
        
        self.setLayout(G_box)
        self.setWindowTitle("Création")
        self.Z_Prop.setDisabled(True)
        if (self.nom!=''):
            self.Tnom.setDisabled(True)
            self.Tprenom.setDisabled(True)
            self.Tage.setDisabled(True)
            self.R_H.setDisabled(True)
            self.R_F.setDisabled(True)
        
        if self.sexe=='H':
            self.R_H.setChecked(True)
            
        
        elif self.sexe=='F':
            self.R_F.setChecked(True)
            
        self.B_return.clicked.connect(self.retour)
        self.B_register.clicked.connect(self.register)
        
    def P_register(self):
        self.nom=self.Tnom.text()
        self.prenom=self.Tprenom.text()
        self.age=self.Tage.text()
        if self.R_F.isChecked():
            #print('Femme')
            self.sexe='F'
            
        elif self.R_H.isChecked():
            #print('Homme')
            self.sexe='H'
        else:
            self.sexe=''
            
        if (self.nom=='' or self.prenom=='' or self.age=='' or self.sexe==''):
            #print('t\'es bloquer')
            self.B_Hist.setToolTip("Veillez à remplir le formulaire avant de cliquer")
            self.B_register.setToolTip("Veillez à remplir le formulaire avant de cliquer")
            return False
        else:
            #print('TRQL')
            self.B_register.setToolTip('Cliquez pour enregistrer le fichier de '+
                                   self.nom+' '+self.prenom)
            self.B_Hist.setToolTip('Cliquez pour accéder à l\'historique de '+
                                   self.nom+' '+self.prenom)
            
            return True
        
    def register(self):
        Possible=self.P_register()
        if Possible:
            #print('tu peux')
            self.fichier=self.nom+'_'+self.prenom+'_'+self.age+'_'+self.sexe+'_.txt'
            #print(self.fichier)
            user=ssh_liste(hostname,port,username,password)
            Liste=user.sendCommand()
            #print(Liste)
            if self.fichier not in Liste:
                crea=ssh_creation(hostname, port, username, password)
                crea.sendCommand(self.fichier)
                with open(self.fichier,'x') as f:
                    f.close()
                
            self.symptome="Symptome : "+self.Z_DialS.toPlainText()
            self.ordonnance="Ordonnance : "+self.Z_DialO.toPlainText()
            registre=ssh_register(hostname, port, username, password)
            registre.sendCommand(self.symptome, self.ordonnance,self.F_local)
            
            self.Z_DialS.clear()
            self.Z_DialO.clear()
                
        else:
            print('tu ne peux pas')
        
    def Medocs(self):
        self.Z_Prop.clear()
        self.Text=self.Z_DialS.toPlainText()
        self.Text=self.Text.split('\n')
        self.mot=[]
        for i in self.Text:
            self.ligne=i.split(' ')
            for j in self.ligne:
                self.mot.append(j)
        self.medicament=[]
        for k in range(len(self.mot)):
            for h in self.repertoire.keys():
                for m in self.repertoire[h]:
                    if self.mot[k]==m:
                        self.medicament.append(h)
                        #print(self.medicament)
                        
        self.medicament=list(set(self.medicament))
        self.resultat=""
        for k in self.medicament:
            self.resultat+=k+'\n'
            
            
        self.Z_Prop.setText(self.resultat)
        
    def retour(self):
        self.hide()
        self.viewA.show()
        
    def historique(self,viewA):
        Possible=self.P_register()
        
        self.fichier=self.nom+'_'+self.prenom+'_'+self.age+'_'+self.sexe+'_.txt'
        user=ssh_liste(hostname,port,username,password)
        Liste=user.sendCommand()
        
        if Possible and self.fichier in Liste:
            #print('tu peux')
            self.hide()
            self.viewH= View_H(viewA,SCP(self.F_local),self.nom,self.prenom,
                               self.age,self.sexe)
        else:
            print('tu ne peux pas')
            self.B_Hist.setToolTip('cette personne n\'est pas enregistrer')
            

class ssh_creation:
    client = None
    
    def __init__(self, hostname, port, username, password):
        try:
            print("Connecting to server.")
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username, 
                                password=password)
    
        except:
            print("Exception raised!")

    def sendCommand(self,F_local):
        if(self.client):
            
            self.client.exec_command("touch "+F_local)
            print('file created!')
            
            
        else:
            print("Connection not opened.")
            
class ssh_register:
    client = None
    
    def __init__(self, hostname, port, username, password):
        try:
            print("Connecting to server.")
            self.client = client.SSHClient()
            self.client.set_missing_host_key_policy(client.AutoAddPolicy())
            self.client.connect(hostname, port=port, username=username, 
                                password=password)
    
        except:
            print("Exception raised!")

    def sendCommand(self,Symptome,Ordonnances,F_local):
        
        if(self.client):
            ajout_S="echo "+Symptome+" >> "+F_local
            ajout_O="echo "+Ordonnances+" >> "+F_local
            ajout_saut="echo ' ' >> "+F_local
            
            self.client.exec_command(ajout_S)
            self.client.exec_command(ajout_O)
            self.client.exec_command(ajout_saut)
            
            print('file uptade!')
            
            
        else:
            print("Connection not opened.")
            
            
class ssh_liste:
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
    


#SshC(hostname, port, username, password)
print(__name__)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    viewC = View_C(ViewA)
    sys.exit(app.exec_())
        