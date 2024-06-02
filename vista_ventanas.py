import sys 
import os
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
from PyQt5.uic import loadUi
import json
from main import* 


class Ventanainicio(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("inicio.ui",self)
        self.coordinador=login_controlador()
        self.setup()
    
    def setup(self):
        self.campo_user.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.campo_password.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9 ]+")))
        self.campo_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.validardatos) 
        self.buttonBox.rejected.connect(self.closeOption)
    

    def validardatos(self):
        username = self.campo_user.text()
        password = self.campo_password.text()
        verificar = self.coordinador.log_in(username,password)

        if isinstance(verificar, tuple):
            self.vetView = Vista()
            self.vetView.show()
            self.close()
        elif existe == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No existe un usuario con los \ndatos proporcionados")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def closeOption(self):
        self.close()

class VentaMenu(QDialog):
    def __init__(self):
        loadUi("ventana resultado.ui",self)
        self.vetController =Coordinador()
        self.setup()
    
    def setup(self):
        self.boton_agregar.clicked.connect(self.abrir_ventana_agregar)
        self.boton_Cdatos.clicked.connect(self.abrir_ventana_Cdatos)
        self.boton_Cestudios.clicked.connect(self.abrir_ventana_Cestudios)
        self.boton_salir.clicked.connect(self.abrir_ventana_salir)
        self.boton_menu.clicked.connect(self.abrir_ventana_menu)
        self.Bagregar_pac.clicked.connect(self.agregar_pac)
        
        self.tabla()
    
    def abrir_ventana_menu(self):
        ventana_menu=self.stackedWidget.setCurrentIndex(0)

    def abrir_ventana_agregar(self):
        ventana_agregar=self.stackedWidget.setCurrentIndex(1)   

    def abrir_ventana_Cdatos(self):
        ventana_Cdatos=self.stackedWidget.setCurrentIndex(2)
        
    def abrir_ventana_Cestudios(self):
        ventana_Cestudios= self.stackedWidget.setCurrentIndex(3) 
        
    def abrir_ventana_salir(self):
        self.ventanaL=ventanaLogin()
        self.ventanaL.show()
        self.close()
    
    def agregar_pac(self):
        nombre = self.nombre.text()
        iden = self.id.text()        
        edad = self.edad.text()
        peso = self.peso.text()
        estatura = self.estatura.text()
        url_I = self.url_imagen.text()
        url_S = self.url_senal.text()
        url_signos = self.url_signos.text()
        
        if not iden or not nombre or not edad or not peso or not estatura or not url_I or not  url_S or not url_signos:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Debe ingresar todos los datos")
            msgBox.setWindowTitle('Datos faltantes')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            isUnique = self.vetController.agregaPac(nombre,)
            self.abrir_ventana_menu()




# app=QApplication(sys.argv)
# mi_vista2=Ventanainicio()
# mi_vista2.show()
# sys.exit(app.exec())