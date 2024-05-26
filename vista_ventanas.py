import sys
import os
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QLineEdit
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import  QRegExpValidator
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi


class Ventanainicio(QMainWindow):
    def __init__(self,ppal=None):
        super().__init__(ppal)
        loadUi("inicio.ui",self)
        self.setup()
    
    def setup(self):
        self.campo_user.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.campo_password.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9 ]+")))
        self.campo_password.setEchoMode(QLineEdit.Password)
        self.buttonBox.accepted.connect(self.validardatos) 
        self.buttonBox.rejected.connect(self.closeOption)

    def setCoordinador(self,c):
        self.__coordinador = c
    

    def validardatos(self):
        pass
        username = self.campo_user.text()
        password = self.campo_password.text()
        verificar = self.__coordinador.validarusuario(username,password)

        if verificar:
            
            self.hide()
            self.newWindow = Vista()
            self.newWindow.setCoordinador(self.__coordinador)
            self.newWindow.show()
    
        else:
            QMessageBox.warning(self, "Error de inicio de sesión", "Usuario o contraseña incorrectos.")
    
    def closeOption(self):
        self.close()

class Vista(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ventana_menu.ui", self)
        self.setup()

    def setup(self):
        self.boton_agregar.clicked.connect(self.load)

    def load(self):
        self.hide()
        self.newWindow = VistaVerDatos()
        self.newWindow.setCoordinador(self.__coordinador2)
        self.newWindow.show()

    def setCoordinador(self, c):
        self.__coordinador2 = c

class VistaVerDatos(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ventana_verdatos.ui", self)
        self.setup()

    def setup(self):
        self.ingresar_nombre.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.ingresar_id.setValidator(QRegExpValidator(QRegExp("[0-9]+")))
        self.ingresar_edad.setValidator(QRegExpValidator(QRegExp("[0-9]+")))
        self.ingresar_altura.setValidator(QDoubleValidator(0.0, 999999.99, 2))
        self.ingresar_peso.setValidator(QRegExpValidator(QRegExp("[0-9]+")))
        

    def setCoordinador(self, c):
        self.__coordinador3 = c