import sys 
import os
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem, QVBoxLayout, QFileDialog, QLabel, QWidget
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QImage, QPixmap
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
from PyQt5.uic import loadUi
import json
from controlador import* 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


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
            self.vetView = VentaMenu()
            self.vetView.show()
            self.close()
        elif verificar == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No existe un usuario con los \ndatos proporcionados")
            msgBox.setWindowTitle('Datos incorrectos')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def closeOption(self):
        self.close()


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot_signals(self, t, signals,min,max):
        self.ax.clear()
        for c in range(8):
            self.ax.plot(t, signals[c,min:max]+10*c)
        self.ax.set_title('Señales del archivo Mat')
        self.ax.set_xlabel('Samples')
        self.ax.set_ylabel('Amplitude')
        self.draw()
    """"
    def plot_signal(self, signal, x_min, x_max, y_min, y_max):
        self.ax.clear()
        self.ax.plot(signal)
        self.ax.set_title('Señal del archivo Mat')
        self.ax.set_xlabel('Samples')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.draw()
        """

class VentaMenu(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ventana resultado.ui",self)
        self.vetController =Coordinador()
        self.setup()

        self.min = 0
        self.max = 20

        self.canvas = MatplotlibCanvas(self.contenedor_senal)
        layout = QVBoxLayout(self.contenedor_senal)
        layout.addWidget(self.canvas)


        
    def setup(self):
        self.boton_agregar.clicked.connect(self.abrir_ventana_agregar)
        self.boton_Cdatos.clicked.connect(self.abrir_ventana_Cdatos)
        self.boton_Cestudios.clicked.connect(self.abrir_ventana_Cestudios)
        self.boton_salir.clicked.connect(self.abrir_ventana_salir)
        self.boton_menu.clicked.connect(self.abrir_ventana_menu)
        self.Bagregar_pac.clicked.connect(self.agregar_pac)
        self.boton_buscar.clicked.connect(self.buscar_paciente)
        self.boton_conteo.clicked.connect(self.abrir_ventana_conteo)
        self.boton_senal.clicked.connect(self.abrir_ventana_senal)
        self.boton_cargar.clicked.connect(self.procesar_senal)
        self.boton_adelante.clicked.connect(self.adelantar_senal)
        self.boton_atras.clicked.connect(self.atrasar_senal)
        self.cargar_img.clicked.connect(self.procesar_img)
        self.url_imagen.clicked.connect(self.cargar_img_archivo)
        self.url_senal.clicked.connect(self.cargar_senal_archivo)
        self.url_signos.clicked.connect(self.cargar_signos_archivo)

    def procesar_senal(self):
        cedula = self.verificar_id.text()
        print(self.min)
        print(self.max)
        t=np.linspace(self.min,self.max,self.max-self.min)
        signals = self.vetController.procesar_senal(cedula,self.min,self.max)
        if signals is not None:
            self.canvas.plot_signals(t, signals,self.min,self.max)
            
        """"
        if signal is not None:
            y_min, y_max = min(signal), max(signal)
            self.canvas.plot_signal(signal, self.min, self.max, y_min, y_max)"""

    def adelantar_senal(self):
        self.min += 20
        self.max += 20
        self.procesar_senal()

    def atrasar_senal(self):
        self.min = max(0, self.min - 20)  
        self.max = max(20, self.max - 20)  
        self.procesar_senal()

    def procesar_img(self):
        cedula = self.verificar_id.text()
        celulas,img = self.vetController.procesar_img(cedula)
        self.conteo_celulas.setText(str(celulas))


        if img is None:
            print("Error al cargar la imgn")
            return
        
        # Verificar y convertir la profundidad de la imagen si es necesario
        if img.dtype != np.uint8:
            img = cv2.convertScaleAbs(img)

        img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    
        # Convertir la imgn de BGR a RGB
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convertir la imgn a formato QImage
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Crear un QLabel y poner la QImage en el QLabel
    
        self.img_label.setPixmap(QPixmap.fromImage(q_img))
        self.img_label.setScaledContents(True)
        
        # Crear un layout y añadir el QLabel al layout
        #layout = QVBoxLayout()
        #layout.addWidget(img_label)
        #self.setLayout(layout)
        
    def cargar_img_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Image Files (*.png *.jpg *.bmp)")
        if filename:
            self.url_imagen.setText(filename)

    def cargar_senal_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de señal", "", "MAT Files (*.mat)")
        if filename:
            self.url_senal.setText(filename)

    def cargar_signos_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de signos vitales", "", "CSV Files (*.csv)")
        if filename:
            self.url_signos.setText(filename)

    def abrir_ventana_menu(self):
        ventana_menu=self.stackedWidget.setCurrentIndex(0)

    def abrir_ventana_agregar(self):
        ventana_agregar=self.stackedWidget.setCurrentIndex(1)   

    def abrir_ventana_Cdatos(self):
        ventana_Cdatos=self.stackedWidget.setCurrentIndex(2)

    def abrir_ventana_Cestudios(self):
        ventana_Cestudios= self.stackedWidget.setCurrentIndex(3)      

    def abrir_ventana_salir(self):
        self.ventanaL=Ventanainicio()
        self.ventanaL.show()
        self.close()

    def abrir_ventana_conteo(self):
        ventana_conteo = self.stackedWidget_2.setCurrentIndex(0)

    def abrir_ventana_senal(self):
        ventana_senal = self.stackedWidget_2.setCurrentIndex(1)

    # Método agregar paciente 
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
            isUnique = self.vetController.agregaPac(nombre,iden,edad,peso,estatura,url_I,url_S,url_signos)
            self.abrir_ventana_menu()
            if not isUnique:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Paciente agregadp")
                msgBox.setWindowTitle('Paciente')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

    # Método buscar pacientes 
    def buscar_paciente(self):
        id_b=self.verificar_id.text()
        if not id_b:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Debe ingresar todos los datos")
            msgBox.setWindowTitle('Datos faltantes')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            resultado= self.vetController.buscarPac(id_b)
            iden,nombre,edad,peso,estatura=resultado
            variables=[nombre,iden,edad,peso,estatura]
            self.tableWidget.setRowCount(1)  # Solo una fila para los valores
            self.tableWidget.setColumnCount(len(variables))  # Una columna por variable
            # Llena la tabla con los datos de las variables
            for col_num, value in enumerate(variables):
                self.tableWidget.setItem(0, col_num, QTableWidgetItem(str(value)))

            # Si quieres asegurarte de que los encabezados están correctos:
            self.tableWidget.setHorizontalHeaderLabels(["nombre", "ID", "edad", "peso", "estatura"])

        try:
            resultado= self.vetController.procesarCsv(id_b)   #datos_pac es una lista
            if resultado is not None:
                promedio, moda, desviacion, datos_pac = resultado
                temperatura=datos_pac[0]
                oxigeno=datos_pac[1]
                frecuencia=datos_pac[2]
                # Configurar el número de filas y columnas una vez fuera del bucle
                self.tableWidget_2.setRowCount(len(temperatura))  
                self.tableWidget_2.setColumnCount(3)  # Tres columnas: temperatura, oxigeno, frecuencia

                # Llena la tabla con los datos de las variables
                for i in range(len(temperatura)):
                    t = temperatura[i]
                    o = oxigeno[i]
                    f = frecuencia[i]
                    lista = [t, o, f]

                    for col_num, value in enumerate(lista):
                        self.tableWidget_2.setItem(i, col_num, QTableWidgetItem(str(value)))

                # Si quieres asegurarte de que los encabezados están correctos:
                self.tableWidget_2.setHorizontalHeaderLabels(["Temperatura", "Oxigeno", "Frecuencia"])

                lista_calculos=[promedio,moda,desviacion]
                self.tableWidget_3.setRowCount(1)  # Solo una fila para los valores
                self.tableWidget_3.setColumnCount(len(lista_calculos))  # Una columna por variable
                # Llena la tabla con los datos de las variables
                for col_num, value in enumerate(lista_calculos):
                    self.tableWidget_3.setItem(0, col_num, QTableWidgetItem(str(value)))

                # Si quieres asegurarte de que los encabezados están correctos:
                self.tableWidget_3.setHorizontalHeaderLabels(["promedion temperatura", "moda oxigenacion", "desviacion frecuencia"])

        except Exception as e:
            print(f"Error al buscar el paciente: {e}")

def main():
    app=QApplication(sys.argv)
    mi_vista2=Ventanainicio()
    mi_vista2.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
