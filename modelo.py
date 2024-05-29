import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPoint, Qt, QByteArray, QIODevice, QBuffer
import sqlite3
from PyQt5.QtCore import QObject
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd

# Clase para crear pacientes 
class Paciente:  
    def __init__(self):  # Se crean todos los atributos relacionados con el paciente
        self.__nombre = ""
        self.__cedula = None
        self.__edad = None
        self.__peso = None
        self.__estatura = None
        self.__urlImagen = ""
        self.__urlSeñal = ""
        self.__urlTablas = ""
    
    # Métodos asignar 
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

    # Métodos ver
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
    
    def leerSeñal(self):
        mat_contents = sio.loadmat(self.__urlSeñal) #loading data
        print("the loaded keys are: " + str(mat_contents.keys())); #the data is loaded as a Python dictionary   
        data = mat_contents['data']   #Se usa solo para archivo señal potencial 
        c,p,e=np.shape(data)      #asigancion de varibles a los valores de shep
        self.__señal_continua= np.reshape(data,(c, p*e),order ='F') # matriz  en 2D
    def verSeñal(self):
        return self.__señal_continua
    def asignarSeñal(self,señal):
        self.__señal_continua=señal

class sistema: 
    def __init__(self, nombre_db):  # Se establece como atributos el nombre de la base de datos, la conexión con la base y el cursor 
        self.nombre_db = nombre_db
        self.conexion = sqlite3.connect(self.nombre_db)
        self.cursor = self.conexion.cursor()

        # Crear la tabla Paciente si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Paciente (
            nombre TEXT, 
            id INTEGER PRIMARY KEY, 
            edad INTEGER, 
            peso REAL, 
            estatura REAL, 
            url_imagen TEXT, 
            url_señal TEXT, 
            url_tablas TEXT)''')
        self.conexion.commit()
        self.cursor.close()

    # Método asignar a paciente en base de datos 
    def asignar_paciente(self, n, c, ed, pe, es, i, s, t):  # Se establecen estos parámetros que vendrán ligados con el controlador y la vista 
        self.cursor = self.conexion.cursor()
        if not self.conexion:  # Verificar inicialmente si se conectó correctamente a la base de datos 
            print("No hay conexión a la base de datos")
            return 
        p = Paciente()  # Se crea objeto paciente para luego usar los métodos de asignación de atributos 
        p.asignar_nombre(n)
        p.asignar_cedula(c)
        p.asignar_edad(ed)
        p.asignar_peso(pe)
        p.asignar_estatura(es)
        p.asignar_urlI(i)
        p.asignar_urlS(s)
        p.asignar_urlT(t)
        
        query_check = "SELECT * FROM Paciente WHERE id = ?"  # Se identifica el parámetro por el cual se va a buscar el paciente 
        self.cursor.execute(query_check, (p.ver_cedula(),))  # Se usa el método ver_cedula de la clase paciente para verificar si el paciente que se quiere ingresar aún no está en la base de datos
        if self.cursor.fetchone() is None:  # Si no se encuentra entonces se usa condicional para agregar paciente 
            query_insert = '''                
            INSERT INTO Paciente (nombre, id, edad, peso, estatura, url_imagen, url_señal, url_tablas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''  # Se hace la identificación de parámetros en la tabla de la base de datos Paciente 
            parametros = (p.ver_nombre(), p.ver_cedula(), p.ver_edad(), p.ver_peso(), p.ver_estatura(), p.ver_urlI(), p.ver_urlS(), p.ver_urlT())
            self.cursor.execute(query_insert, parametros)  # Se relaciona el query_insert con la tupla de parámetros del paciente
            self.conexion.commit()
            self.cursor.close()
            print(f"Paciente con la cédula {p.ver_cedula()} agregado a la base de datos")  # Retorno de mensaje para verificar en consola la ejecución del código 
        else:
            print(f"Paciente con la cédula {p.ver_cedula()} ya existe en la base de datos")
            self.cursor.close()

    # Método para contar células en una imagen
    def contar_celulas(self, cedula):
        if not self.conexion:
            print("No hay conexión a la base de datos")
            return
        
        self.cursor = self.conexion.cursor() # Se inicializa el cursor

        # Obtener la URL de la imagen del paciente desde la base de datos
        query_url = "SELECT url_imagen FROM Paciente WHERE id = ?"
        self.cursor.execute(query_url, (cedula,))
        result = self.cursor.fetchone()
        if result is None:
            print(f"Paciente con la cédula {cedula} no encontrado en la base de datos")
            self.cursor.close() # Se cierra el cursor
            return

        url_imagen = result[0]
        print(f"Ruta de la imagen: {url_imagen}")

        # Cargar y procesar la imagen
        img = cv2.imread(url_imagen)
        if img is None:
            print(f"No se pudo cargar la imagen en la ruta: {url_imagen}")
            self.cursor.close() # Se cierra el cursor
            return
        
        self.cursor.close() # Se cierra el cursor

        plt.subplot(3, 2, 1)
        plt.title('Imagen sin transformación')
        plt.axis('off')
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Convertir a escala de grises y aplicar umbral
        imapB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, imapB = cv2.threshold(imapB, 127, 255, cv2.THRESH_BINARY)
        plt.subplot(3, 2, 2)
        plt.title('Imagen binaria')
        plt.axis('off')
        plt.imshow(imapB, cmap='gray', vmin=0, vmax=255)
        
        # Apertura, dilatación y erosión
        kernel = np.ones((5, 5), np.uint8)
        imapB = cv2.morphologyEx(imapB, cv2.MORPH_OPEN, kernel) 
        ima2 = cv2.dilate(imapB, kernel, iterations=2)
        ima2 = cv2.erode(ima2, kernel, iterations=2)
        num_cells, labeled_image = cv2.connectedComponents(ima2)

        # Imprimir el número de células
        print("Número de células encontradas:", num_cells - 1)  # Restamos 1 para excluir el fondo

        # Graficar el resultado
        plt.subplot(3, 2, 3)
        plt.imshow(labeled_image, cmap='jet')  # Usamos 'jet' colormap para visualizar las etiquetas
        plt.title('Imagen con células etiquetadas')
        plt.axis('off')
        plt.show()
    
    # Método para procesar archivo CSV
    def procesar_csv(self, cedula):
        if not self.conexion:
            print("No hay conexión a la base de datos")
            return
        
        self.cursor = self.conexion.cursor() # Se inicializa el cursor

        # Obtener la URL del archivo CSV del paciente desde la base de datos
        query_url = "SELECT url_tablas FROM Paciente WHERE id = ?"
        self.cursor.execute(query_url, (cedula,))
        result = self.cursor.fetchone()
        if result is None:
            print(f"Paciente con la cédula {cedula} no encontrado en la base de datos")
            self.cursor.close() # Se cierra el cursor
            return

        url_tablas = result[0]
        print(f"Ruta del archivo CSV: {url_tablas}")

        # Leer el archivo CSV
        try:
            data = pd.read_csv(url_tablas)
        except Exception as e:
            print(f"No se pudo leer el archivo CSV en la ruta: {url_tablas}. Error: {e}")
            self.cursor.close() # Se cierra el cursor
            return
        
        self.cursor.close() # Se cierra el cursor

        # Mostrar la tabla
        print("Contenido del archivo CSV:")
        print(data)

        # Calcular estadisticas
        promedio_col1 = data.iloc[:, 0].mean()
        moda_col2 = data.iloc[:, 1].mode()[0]
        desviacion_col3 = data.iloc[:, 2].std()

        print(f"Promedio de la Temperatura: {promedio_col1}")
        print(f"Moda de la Oxigenación en sangre: {moda_col2}")
        print(f"Desviación de la Frecuencia Cardiaca: {desviacion_col3}")

        return promedio_col1, moda_col2, desviacion_col3

#sis = sistema('app.db')
#sis.asignar_paciente('Pablo', 73, 19, 80, 1.8, r'globulosrojos.jpg', 'señal', 'signosvit.csv')
#sis.contar_celulas(88)
#promedio, moda, desviacion = sis.procesar_csv(73)

class loging(QObject):
    def __init__(self):
        super().__init__()
        self.__login = '' #loging 
        self.__password = '' 
        self.__diccpacientes = {}

    def validaruser(self, l, p):
        return self.__login == l and self.__password == p

    def set_path(self, f): 
        self.__carpeta = f

    def get_diccpacientes (self):
        return self.__diccpacientes

    def datos_pacientes(self, id, nombre, edad, altura, peso):
        self.__diccpacientes[id] = {
            'nombre': nombre,
            'edad': edad,
            'altura': altura,
            'peso': peso
        }