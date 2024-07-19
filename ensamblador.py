from ejecutable import Ejecutable
import re

class Ensamblador:
    def __init__(self):
        self.posicion = 0
    
    def ensamblar(self, nombreArchivo):
        resultado = Ejecutable()
        self.ensamblar2(nombreArchivo, resultado)
        self.posicion = 0
        return resultado
    
    def ensamblar2(self, nombreArchivo, ejecutable):
        with open(nombreArchivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip().lower()
    
                if not linea or linea.startswith(';'):
                    continue
                
                coincidencia = self.buscar_include(linea)
                if coincidencia:
                    archivo_incluido = coincidencia.group(1)
                    ejecutable.agregar_codigo(linea)
                    ejecutable.agregar_noop(linea)
                    self.posicion += 1
                    self.ensamblar2(archivo_incluido, ejecutable)
                    continue
                
                coincidencia = self.buscar_entrypoint(linea)
                if coincidencia:
                    ejecutable.agregar_codigo(linea)
                    linea = coincidencia.group().strip(':')
                    ejecutable.agregar_entryPoint(linea, self.posicion)
                    self.posicion += 1
                    continue
                
                coincidencia = self.buscar_etiqueta(linea)
                if coincidencia:
                    etiqueta = coincidencia.group().strip(':')
                    ejecutable.agregar_etiqueta(etiqueta, self.posicion)
                
                coincidencia = self.buscar_instruccion1(linea)
                if coincidencia:
                    instruccion_nombre = coincidencia.group(1)
                    parametro = [coincidencia.group(2)]
                    ejecutable.procesar_instruccion(instruccion_nombre, *parametro)
                    ejecutable.agregar_codigo(linea)
                    self.posicion += 1
                    continue

                coincidencia = self.buscar_instruccion2(linea)
                if coincidencia:
                    instruccion_nombre = coincidencia.group(1)
                    parametros = [coincidencia.group(2), coincidencia.group(3)]
                    ejecutable.procesar_instruccion(instruccion_nombre, *parametros)
                    ejecutable.agregar_codigo(linea)
                    self.posicion += 1
                    continue
                
                if linea == 'ret' or linea == "clearflags":
                    ejecutable.procesar_instruccion(linea)
                    ejecutable.agregar_codigo(linea)
                    self.posicion += 1
                    continue
                
                ejecutable.agregar_codigo(linea)
                self.posicion += 1

    def buscar_entrypoint(self, linea):
        patron_entrypoint = r'\b(main|_start):'
        return re.search(patron_entrypoint, linea)

    def buscar_etiqueta(self, linea):
        patron_etiqueta = r'\b\w+:'
        return re.search(patron_etiqueta, linea)

    def buscar_include(self, linea):
        patron_include = r'\binclude\s+"([^"]+)"'
        return re.search(patron_include, linea)

    def buscar_instruccion1(self, linea):
        #Busca la instruccion con 1 operando
        patron_instruccion1 = r'^(\w+)\s+([^;\s]+)$'
        return re.match(patron_instruccion1, linea)

    def buscar_instruccion2(self, linea):
        #Busca la instruccion con 2 operandos
        patron_instruccion2 = r'^(\w+)\s+([^,\s]+),\s*([^;\s]+)$'
        return re.match(patron_instruccion2, linea)


def show(ejecutable):
    print("Valor del entryPoint: ", ejecutable.entryPoint)
    print("Codigo fuente: ",ejecutable.codigo,'\n')
    print("LookupTable: ",ejecutable.lookupTable, '\n')
    for i, instruccion in enumerate(ejecutable.instrucciones):
        print(i, "- ", instruccion)
        

if __name__ == '__main__':
    ensamblador = Ensamblador()
    ejecutable = ensamblador.ensamblar('archivo.asm')
    show(ejecutable)
