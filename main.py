from modelo import loging
from vista_ventanas import Ventanainicio
import sys
from PyQt5.QtWidgets import QApplication

class Coordinador(object):
    def __init__(self,vista,modelo):
        self.__mi_vista = vista
        self.__mi_modelo = modelo

    def validarusuario(self,l,p):
        return self.__mi_modelo.validaruser(l,p)
    
#def datos_paciente(self, id, nombre, edad, altura, peso):
       # return self.__mi_modelo.datos_pacientes(id, nombre, edad, altura, peso)

def main():

    app = QApplication(sys.argv)
    mi_vista = Ventanainicio()
    mi_modelo = loging()
    mi_coordinador = Coordinador(mi_vista,mi_modelo)
    mi_vista.setCoordinador(mi_coordinador)
    mi_vista.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()