from proceso import Proceso
from estado import Estado
import time

class SistemaOperativo:
    def __init__(self, lista_ejecutables, procesador):
        self.procesador = procesador
        self.procesador.set_sisOp(self)
        self.procesos = [Proceso(ejecutable) for ejecutable in lista_ejecutables]
        self.iterador = 0  
        self.contador_instrucciones = 0
        self.rafaga = 3
        # Iniciar el primer proceso
        self.procesador.ejecutar_proceso(self.procesos[self.iterador])
    
    def clock_handler(self):
        self.contador_instrucciones += 1

        # si el proceso actual ha finalizado
        if self.procesador.get_registro('ip') >= len(self.proceso_actual().ejecutable.instrucciones):
            print("FINALIZO PROCESO")
            self.proceso_actual().finalizar()
            self.contador_instrucciones = 0
            if not self.todos_procesos_finalizados():
                print("CAMBIO")
                self.iterador = (self.iterador + 1) % len(self.procesos)
                self.procesador.ejecutar_proceso(self.procesos[self.iterador])
            else:
                self.procesador.estado = Estado.FINALIZADO

        if self.procesos_pendientes() == 1:
            pass

        # Cambiar de proceso después de la rafaga de instrucciones
        elif self.contador_instrucciones >= self.rafaga and self.cantidad_restante_instrucciones() > self.rafaga and self.proceso_actual().estado != Estado.FINALIZADO:
            self.contador_instrucciones = 0
            self.proceso_actual().guardar_contexto(self.procesador)
            self.proceso_actual().bloquear()
            
            # rotacion round robin
            # 2%3 = 
            self.iterador = (self.iterador + 1) % len(self.procesos)
            
            proceso_nuevo = self.procesos[self.iterador]
            if self.proceso_actual().estado == Estado.EJECUCION:
                self.procesador.ejecutar_proceso(proceso_nuevo)
                self.procesador.cambiarIP(proceso_nuevo.ejecutable.entryPoint)
            elif self.proceso_actual().estado == Estado.BLOQUEADO:
                self.procesador.ejecutar_proceso(proceso_nuevo)
        else:
            pass


    def proceso_actual(self):
        return self.procesos[self.iterador]

    def procesos_pendientes(self):
        return sum(1 for proceso in self.procesos if proceso.estado != Estado.FINALIZADO)
    
    def todos_procesos_finalizados(self):
        return all(proceso.estado == Estado.FINALIZADO for proceso in self.procesos)
    
    def cantidad_restante_instrucciones(self):
        return len(self.procesos[self.iterador].ejecutable.instrucciones) - self.procesador.registros['ip']
    
    def syscallHandler(self,servicio, parametros):
        if(servicio == 1):
            valor = parametros[0]
            fila = parametros[1]
            columna = parametros[2]
            self.proceso_actual().pantalla[fila][columna] = valor
        
