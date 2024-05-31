import sys
import os
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QLineEdit, QTableWidgetItem
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import  QRegExpValidator
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
import pandas as pd


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
        self.buttonBox.accepted.connect(self.validardatos) 
        self.buttonBox.rejected.connect(self.closeOption)

    def validardatos(self):
        pass
    
    def closeOption(self):
        self.hide()
        self.newWindow = Vista()
        self.newWindow.setCoordinador(self.__coordinador3)
        self.newWindow.show()

    def setCoordinador(self, c):
        self.__coordinador3 = c


# Copie de aquí hasta el final 8==================================================D
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
        id = int(self.verificar_id.text())
        print(type(id))
        print(id)
        cedula = self.__coordinador2.obtener_datos(id)
        if cedula is None:
            QMessageBox.warning(self, "Advertencia", "Cédula incorrecta")
        else:
            self.hide()
            self.newWindow = VistaVerDatos(id, self.__coordinador2)
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
    def __init__(self,cedula,coordinador):
        super().__init__()
        self.cedula = cedula
        self.__coordinador3 = coordinador
        loadUi("ventana_verdatos.ui", self)
        self.setup()

    def setup(self):
        self.salir_de_ventana.clicked.connect(self.close)

        nombre,id, edad, altura, peso = self.__coordinador3.obtener_datos(self.cedula)

        self.datos_paciente.setRowCount(5)
        self.datos_paciente.setColumnCount(1)
        self.datos_paciente.setItem(0, 0, QTableWidgetItem(str(id)))
        self.datos_paciente.setItem(1, 0, QTableWidgetItem(str(nombre)))
        self.datos_paciente.setItem(2, 0, QTableWidgetItem(str(edad)))
        self.datos_paciente.setItem(3, 0, QTableWidgetItem(str(altura)))
        self.datos_paciente.setItem(4, 0, QTableWidgetItem(str(peso)))

        promedio_col1, moda_col2, desviacion_col3, signosvit = self.__coordinador3.procesar_csv(self.cedula)
        print(signosvit)
        temperatura = signosvit[0]
        oxigeno = signosvit[1]
        fcardiaca = signosvit[2]

        self.tabla_signos.clearContents()
        self.tabla_signos.setRowCount(len(temperatura))

        for i in range(len(temperatura)):
            self.tabla_signos.setItem(i, 0, QTableWidgetItem(str(temperatura[i])))  # Temperatura in column 0
            self.tabla_signos.setItem(i, 1, QTableWidgetItem(str(oxigeno[i])))      # Oxígeno in column 1
            self.tabla_signos.setItem(i, 2, QTableWidgetItem(str(fcardiaca[i])))     # Frecuencia cardíaca in column 2

        promedio_col1 = f"{promedio_col1:.2f}"
        moda_col2 = f"{moda_col2:.2f}"
        desviacion_col3 = f"{desviacion_col3:.2f}"


        self.tableWidget_2.setRowCount(3)
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setItem(0, 0, QTableWidgetItem(promedio_col1))
        self.tableWidget_2.setItem(1, 0, QTableWidgetItem(moda_col2))
        self.tableWidget_2.setItem(2, 0, QTableWidgetItem(desviacion_col3))

    def setCoordinador(self, c):
        self.__coordinador = c
        
    def close (self):
        self.hide()
        self.lastWindow = Vista()
        self.lastWindow.setCoordinador(self.__coordinador)
        self.lastWindow.show()
        

