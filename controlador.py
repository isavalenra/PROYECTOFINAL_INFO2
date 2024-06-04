from modelo import*
class login_controlador:
    def __init__(self):
        self.user_model=LoginModelo()
        
    def log_in(self, username:str, password:str):
        result = self.user_model.existe(username, password)
        return result
class Coordinador():
    def __init__(self):
        self.mi_modelo = sistema()
    
    def agregaPac(self, n, c, ed, pe, es, i, s, t):
        return self.mi_modelo.asignar_paciente( n, c, ed, pe, es, i, s, t)
    
    def buscarPac(self,cedula):
        return self.mi_modelo.obtener_datos_paciente(cedula)
    
    def procesarCsv(self,cedula):
        return self.mi_modelo.procesar_csv(cedula)
    
    def procesar_senal(self,cedula,min,max):
        return self.mi_modelo.procesar_senal(cedula,min,max)
    
    def procesar_img(self,cedula):
        return self.mi_modelo.contar_celulas(cedula)



