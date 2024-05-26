import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPoint, Qt, QByteArray, QIODevice, QBuffer
import sqlite3
from PyQt5.QtCore import QObject
import os

# Establecer base de datos, hacer conexion y desconexion 
class BaseDatos:
    def __init__(self, nombre_db):
        self.nombre_db = nombre_db
        self.conexion = None
        self.cursor = None
    
    def realizar_conexion(self):  # Se realiza la conexion 
        self.conexion = sqlite3.connect(self.nombre_db)
        self.cursor = self.conexion.cursor()
        print("La conexion se realizo exitosamente")
    
    def desconexion(self):  # Se realiza la desconexion 
        if self.conexion:
            self.conexion.close()
            print(f"Se desconecto de la base de datos: {self.nombre_db}")

class Paciente(BaseDatos):    # Clase para crear pacientes 
    def __init__(self, nombre_db):
        super().__init__(nombre_db)
        self.__nombre = ""
        self.__cedula = None
        self.__edad = None
        self.__peso = None
        self.__estatura = None
        self.__urlImagen = ""
        self.__urlSeñal = ""
        self.__urlTablas = ""
    
    # Metodos asignar 
    def asignar_nombre(self, nombre):
        self.__nombre = nombre
    def asignar_cedula(self, id):
        self.__cedula = id
    def asignar_edad(self, edad):
        self.__edad = edad
    def asignar_peso(self, peso):
        self.__peso = peso
    def asignar_estatura(self, estatura):
        self.__estatura = estatura
    def asignar_urlI(self, urlI):
        self.__urlImagen = urlI
    def asignar_urlS(self, urlS):
        self.__urlSeñal = urlS
    def asignar_urlT(self, urlT):
        self.__urlTablas = urlT

    # Metodos ver
    def ver_nombre(self):
        return self.__nombre
    def ver_cedula(self):
        return self.__cedula
    def ver_edad(self):
        return self.__edad
    def ver_peso(self):
        return self.__peso
    def ver_estatura(self):
        return self.__estatura
    def ver_urlI(self):
        return self.__urlImagen
    def ver_urlS(self):
        return self.__urlSeñal
    def ver_urlT(self):
        return self.__urlTablas
    
    # Metodo asignar a paciente en base de datos 
    def asignar_paciente(self):
        if not self.conexion:
            print("No hay conexion a la base de datos")
            return 
        
        query_check = "SELECT * FROM Paciente WHERE ID = ?"
        self.cursor.execute(query_check, (self.__cedula,))
        if self.cursor.fetchone() is None:
            query_insert = '''
            INSERT INTO Paciente (nombre, id, edad, peso, estatura, url_imagen, url_señal, url_tablas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            parametros = (self.__nombre, self.__cedula, self.__edad, self.__peso, self.__estatura, self.__urlImagen, self.__urlSeñal, self.__urlTablas)
            self.cursor.execute(query_insert, parametros)
            self.conexion.commit()
            print(f"Paciente con la cedula {self.__cedula} agregado a la base de datos")
        else:
            print(f"Paciente con la cedula {self.__cedula} ya existe en la base de datos")

# Uso del código

paciente = Paciente('app.db')
paciente.asignar_nombre('juana')
paciente.asignar_cedula(0000)
paciente.asignar_edad(30)
paciente.asignar_peso(70)
paciente.asignar_estatura(1.80)
paciente.asignar_urlI('img_url')
paciente.asignar_urlS('img_señal')
paciente.asignar_urlT('img_tabla')
paciente.realizar_conexion() 
paciente.asignar_paciente()
paciente.desconexion()

class loging(QObject):
    def __init__(self):
        super().__init__()
        self.__login = '' #loging 
        self.__password = '' 
        self.__carpeta = ""

    def validaruser(self, l, p):
        return self.__login == l and self.__password == p

    def get_path(self, f): 
        self.__carpeta = f