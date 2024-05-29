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
        self.boton_agregar.clicked.connect(self.open)
        self.boton_salir.clicked.connect(self.close)
        self.boton_consultar.clicked.connect(self.search)

    def open(self):
        self.hide()
        self.newWindow = VistaVentanaAgregar()
        self.newWindow.setCoordinador(self.__coordinador2)
        self.newWindow.show()

    def search(self):
        self.hide()
        self.newWindow = VentanaBusqueda()
        self.newWindow.setCoordinador(self.__coordinador2)
        self.newWindow.show()

    def setCoordinador(self, c):
        self.__coordinador2 = c

    def close (self):
        self.hide()
        self.lastWindow = Ventanainicio()
        self.lastWindow.setCoordinador(self.__coordinador2)
        self.lastWindow.show()

class VistaVentanaAgregar(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ventana_agregar.ui", self)
        self.setup()

    def setup(self):
        pass   

class VentanaBusqueda(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ventana_busqueda.ui", self)
        self.setup()  

    def setup(self):
        self.buttonBox.accepted.connect(self.validardatos) 
        self.buttonBox.rejected.connect(self.closeOption)
        self.verificar_id.setValidator(QRegExpValidator(QRegExp("[0-9]+")))
    
    def validardatos(self):
        self.hide()
        self.newWindow = VistaVerDatos()
        self.newWindow.setCoordinador(self.__coordinador2)
        self.newWindow.show()
    
    def closeOption(self):
        self.hide()
        self.newWindow = Vista()
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
        self.salir_de_ventana.clicked.connect(self.close)
        self.agregar_datos.clicked.connect(self.save)

    def save(self):
        id = self.ingresar_id.text()
        nombre = self.ingresar_nombre.text()
        edad = self.ingresar_edad.text()
        altura = self.ingresar_altura.text()
        peso = self.ingresar_peso.text()

        if not id or not nombre or not edad or not altura or not peso:
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben estar llenos.")

        else:   
            self.__coordinador3.datos_paciente(id, nombre, edad, altura, peso)
            QMessageBox.information(self, "Guardado", "Datos guardados correctamente")
        
    def close (self):
        self.hide()
        self.lastWindow = Vista()
        self.lastWindow.setCoordinador(self.__coordinador3)
        self.lastWindow.show()
        

    def setCoordinador(self, c):
        self.__coordinador3 = c