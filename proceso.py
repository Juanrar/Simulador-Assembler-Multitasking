from estado import Estado
import numpy as np

class Proceso:
    def __init__(self, ejecutable):
        self.ejecutable = ejecutable
        self.contexto = {
            'ax': 0, 'bx': 0, 'cx': 0, 'dx': 0, 'ip': 0, 'ZF': 0, 'CF':0
        }
        self.estado = Estado.EJECUCION
        self.pantalla = np.zeros((10, 10))
    
    def guardar_contexto(self, procesador):
        self.contexto['ax'] = procesador.get_registro('ax')
        self.contexto['bx'] = procesador.get_registro('bx')
        self.contexto['cx'] = procesador.get_registro('cx')
        self.contexto['dx'] = procesador.get_registro('dx')
        self.contexto['ip'] = procesador.get_registro('ip')
        self.contexto['ZF'] = procesador.get_registro('ZF')
        self.contexto['CF'] = procesador.get_registro('CF')

    
    def restaurar_contexto(self, procesador):
        procesador.set_registro('ax', self.contexto['ax'])
        procesador.set_registro('bx', self.contexto['bx'])
        procesador.set_registro('cx', self.contexto['cx'])
        procesador.set_registro('dx', self.contexto['dx'])
        procesador.set_registro('ip', self.contexto['ip'])
        procesador.set_registro('ZF', self.contexto['ZF'])
        procesador.set_registro('CF', self.contexto['CF'])

    
    def finalizar(self):
        self.estado = Estado.FINALIZADO
    
    def bloquear(self):
        self.estado = Estado.BLOQUEADO
    
    def activar(self):
        self.estado = Estado.EJECUCION