import time
from visualizador import Visualizador
from instruccion import Ret
from sistemaOperativo import SistemaOperativo
from estado import Estado
import keyboard

class Procesador: 
    
    def __init__(self):
        self.registros = {'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0, 'ip': 0, 'ZF': 0, 'CF':0}
        self.sistemaOperativo = None
        self.proceso_actual = None
        self.estado = Estado.EJECUCION

    def get_registro(self, nombre_registro):
        return self.registros.get(nombre_registro, None)

    def set_registro(self, nombre_registro, valor):
        if nombre_registro in self.registros:
            self.registros[nombre_registro] = valor
        else:
            raise ValueError(f"Registro incorrecto ", nombre_registro)
        
    def set_sisOp(self,sistemaOperativo):
        self.sistemaOperativo = sistemaOperativo
    
    def get_sisOp(self):
        return self.sistemaOperativo
        
    def incremetarIP(self):
        self.registros['ip'] += 1
    
    def cambiarIP(self, posicion):
        self.registros['ip'] = posicion
        
    def ejecutar_proceso(self, proceso):
        self.proceso_actual = proceso
        proceso.restaurar_contexto(self)

    def procesar(self):
        self.cambiarIP(self.proceso_actual.ejecutable.entryPoint)
        visualizador = Visualizador(self)
        while self.estado == Estado.EJECUCION:
            instruccion_actual = self.proceso_actual.ejecutable.instrucciones[self.registros['ip']]
            instruccion_actual.procesar(self)
            
            if isinstance(instruccion_actual, Ret):
                continue
            else:
                self.incremetarIP()

            visualizador.mostrar_pantalla(self.proceso_actual.ejecutable)
            self.sistemaOperativo.clock_handler()
            keyboard.wait('space')
 
        if self.sistemaOperativo.todos_procesos_finalizados():
            print("LISTA DE PROCESOS FINALIZADA")
        
        

if __name__ == '__main__':
    # Creamos una instancia del procesador
    procesador = Procesador()
    
    # Configuramos algunos registros para el ejemplo
    procesador.set_registro('ax', 10)
    procesador.set_registro('bx', 5)
    
    # Mostramos el estado final de los registros
    print("Estado final de los registros:")
    print("ax:", procesador.get_registro('ax'))
    print("bx:", procesador.get_registro('bx'))
    print("cx:", procesador.get_registro('cx'))
    print("dx:", procesador.get_registro('dx'))
    print("ip:", procesador.get_registro('ip'))
    print("flag:", procesador.get_registro('flag'))
    print("registro falso 1: ", procesador.get_registro(0))
    print("registro falso 2: ", procesador.get_registro('aaaaa'))
