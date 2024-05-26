import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPoint, Qt, QByteArray, QIODevice, QBuffer
import sqlite3
from PyQt5.QtCore import QObject
import os

# Establecer base de datos, hacer conexion y desconexion 
class Paciente():    # Clase para crear pacientes 
    def __init__(self):   #se crean todos los atributos relacionados con el paciente
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

class sistema(): 
    def __init__(self,nombre_db):   #Se esatblece como atributos el nombre de la base de datos, las conexion con la base  y el cursor 
        self.nombre_db = nombre_db
        self.conexion =sqlite3.connect(self.nombre_db)
        self.cursor =self.conexion.cursor()

    # Metodo asignar a paciente en base de datos 
    def asignar_paciente(self,n,c,ed,pe,es,i,s,t):  #Seestablecen esto parametros qeu vendran ligados con el controlador y la vista 
        if not self.conexion:  #Verificar inicialmente si se conecto correctamente a la base de datos 
            print("No hay conexion a la base de datos")
            return 
        p=Paciente()   #Se crea obejto paciente para luego usar los metodos de asiganacion de atributos 
        p.asignar_nombre(n)
        p.asignar_cedula(c)
        p.asignar_edad(ed)
        p.asignar_peso(pe)
        p.asignar_estatura(es)
        p.asignar_urlI(i)
        p.asignar_urlS(s)
        p.asignar_urlT(t)
        

        query_check = "SELECT * FROM Paciente WHERE ID = ?"  #Se identifica el parametro por el cual se va a bucar el paciente 
        self.cursor.execute(query_check, (p.ver_cedula(),))   #Se usa el metod ver_cedula de la clase paciente para verificar si el paciente que se quiere ingresar aun no esta en la base de datos 
        if self.cursor.fetchone() is None:  #si no se encuentra enotonce se usa condiconal para agregar paciente 
            query_insert = '''                
            INSERT INTO Paciente (nombre, id, edad, peso, estatura, url_imagen, url_señal, url_tablas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''   #Se hace el la identificacion de parametros en la tabla de la base de datos Paciente 
            parametros = (p.ver_nombre(),p.ver_cedula(),p.ver_edad(),p.ver_peso(),p.ver_estatura(),p.ver_urlI(),p.ver_urlS(),p.ver_urlT())
            self.cursor.execute(query_insert, parametros)  #se relaciona el query_insert con la tupla de parametros del paciente
            self.conexion.commit()
            self.conexion.close()
            print(f"Paciente con la cedula {p.ver_cedula()} agregado a la base de datos")   #Retono de mesaje para verificar en consola la ejecucion del codigo 
        else:
            print(f"Paciente con la cedula {p.ver_cedula()} ya existe en la base de datos")


sis=sistema('app.db')
sis.asignar_paciente('juan',50,19,80, 1.8,'imagen','señal','tabla')


