from modelo import*
class login_controlador:
    def __init__(self):
        self.user_model=LoginModelo()
        
    def log_in(self, username:str, password:str):
        result = self.user_model.existe(username, password)
        return result
class Coordinador(object):
    def __init__(self,vista,modelo):
        self.__mi_vista = vista
        self.__mi_modelo = modelo

    def validarusuario(self,l,p):
        return self.__mi_modelo.validaruser(l,p)
    
    def datos_paciente(self, id, nombre, edad, altura, peso):
        return self.__mi_modelo.datos_pacientes(id, nombre, edad, altura, peso)
    
    def obtener_datos(self,cedula):
        return self.__mi_modelo.obtener_datos_paciente(cedula)
    
    def procesar_csv (self,cedula):
        return self.__mi_modelo.procesar_csv(cedula)


