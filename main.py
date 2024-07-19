from ensamblador import Ensamblador
from procesador import Procesador
from sistemaOperativo import SistemaOperativo

if __name__ == '__main__':
    ensamblador = Ensamblador()
    ejecutable1 = ensamblador.ensamblar('archivo.asm')
    procesador = Procesador()
    sistemaOperativo = SistemaOperativo([ejecutable1],procesador)
    
    procesador.procesar()