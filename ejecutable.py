from instruccion import Mov,Add,Jmp,Jnz,Jnc,Cmp,Inc,Dec,Noop,Pop,Push,Call,Ret,Int,Neg,Jle,Sub,ClearFlags

class Ejecutable:
    entryPoint = 0
    
    def __init__(self):
        self.codigo = []
        self.instrucciones = []
        self.lookupTable = {}
        self.pila= []
        
    def agregar_codigo(self,codigo):
        self.codigo.append(codigo)
        
    def agregar_noop(self, etiqueta):
        self.instrucciones.append(Noop(etiqueta))
        
    def agregar_etiqueta(self, etiqueta, posicion):
        self.lookupTable[etiqueta] = posicion
        self.instrucciones.append(Noop(etiqueta))
        
    def agregar_entryPoint(self, linea, posicion):
        self.lookupTable[linea] = posicion
        self.entryPoint = posicion
        self.instrucciones.append(Noop(linea))
        
    def procesar_instruccion(self, instruccion, *args):
        instrucciones_disponibles = {
            'mov': Mov,
            'add': Add,
            'jmp': Jmp,
            'jnz': Jnz,
            'jnc': Jnc,
            'cmp': Cmp,
            'inc': Inc,
            'dec': Dec,
            'pop': Pop,
            'call': Call,
            'push': Push,
            'ret': Ret,
            'int': Int,
            'neg': Neg,
            'jle': Jle,
            'sub': Sub,
            'clearflags': ClearFlags
        }
        
        if instruccion in instrucciones_disponibles:
            clase_instruccion = instrucciones_disponibles[instruccion]
            if clase_instruccion in [Mov, Add, Cmp, Sub]:
                # Si la instrucción es Mov, Add o Cmp, esperamos que se pasen 2 argumentos
                if len(args) != 2:
                    raise ValueError(f"Instrucción {instruccion} requiere 2 argumentos")
                self.instrucciones.append(clase_instruccion(*args))
            elif clase_instruccion in [Jmp, Jnz, Jnc, Call, Push, Pop, Jle]:
                # Si la instrucción es Jmp o Jnz, esperamos que se pase 2 argumento
                if len(args) != 1:
                    raise ValueError(f"Instrucción {instruccion} requiere 2 argumentos")
                self.instrucciones.append(clase_instruccion(self,*args))
            elif clase_instruccion in [Inc, Dec, Int, Neg]:
                # Si la instrucción es Inc o Dec, esperamos que se pase 1 argumento
                if len(args) != 1:
                    raise ValueError(f"Instrucción {instruccion} requiere 1 argumentos")
                self.instrucciones.append(clase_instruccion(*args))
            elif clase_instruccion == Ret or clase_instruccion == ClearFlags:
                self.instrucciones.append(clase_instruccion(self))
        else:
            raise ValueError("Instrucción no válida:", instruccion)

            
if __name__ == "__main__":
    # Crear una instancia de Ejecutable
    ejecutable = Ejecutable()

    # Agregar algunas instrucciones
    ejecutable.agregar_etiqueta('aaaa',4)
    ejecutable.procesar_instruccion('call','aaaa')
    ejecutable.procesar_instruccion('ret')
    
    #print(ejecutable.instrucciones)
    
    print(ejecutable.instrucciones)
    for instruccion in ejecutable.instrucciones:
        print(instruccion)
    print(ejecutable.lookupTable)
    
    