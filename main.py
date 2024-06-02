from modelo import*
class login_controlador:
    def __init__(self):
        self.user_model=LoginModelo()
        
    def log_in(self, username:str, password:str):
        result = self.user_model.existe(username, password)
        return result
class Coordinador():
    def __init__(self):
        self.__mi_modelo = sistema()
    
    def agregaPac(self, n, c, ed, pe, es, i, s, t):
        return self.__mi_modelo.asignar_paciente( n, c, ed, pe, es, i, s, t)



