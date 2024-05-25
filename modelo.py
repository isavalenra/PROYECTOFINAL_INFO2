import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPoint, Qt, QByteArray, QIODevice, QBuffer

#Establecer base de datos, hacer conexion y desconexion 

class BaseDatos:
    def __init__(self,nombre_db):
        self.nombre_db=nombre_db
        self.conexion=None
        self.cursor=None
    
    def conexion(self):  #Se realiza la conexion 
        self.conexion=sqlite3.connect(self.nombre_db)
        self.cursor=self.conexion.cursor()
        print("La conexion se realizo exitosamente")
    
    def desconexion(self):  #se realiza la desconexion 
        if self.conexion:
            self.conexion.close()
            print(f"Se desconecto de la base de datos:{self.nombre_db}")