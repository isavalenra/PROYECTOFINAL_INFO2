import sys 
import os
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
from PyQt5.uic import loadUi
import json
from main import* 
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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

    def plot_signal(self, signal):
        self.ax.clear()
        self.ax.plot(signal)
        self.ax.set_title('Signal from .mat file')
        self.ax.set_xlabel('Samples')
        self.ax.set_ylabel('Amplitude')
        self.draw()


class VentaMenu(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ventana resultado.ui",self)
        self.vetController =Coordinador()
        self.setup()

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

    def procesar_senal(self):
        cedula = self.guardar_cedula.text()
        signal = self.vetController.procesar_senal(cedula)
        if signal is not None:
            self.canvas.plot_signal(signal)



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

    #Metodo agregar paciente 
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
    #Metodo buscar pacientes 
    def buscar_paciente(self):
        id_b=self.verificar_id.text()
        if not id :
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