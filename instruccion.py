class Instruccion:
    def procesar(self, procesador):
        pass

#Clases de Instrucciones 
class Mov(Instruccion):

    # Mover un valor literal o el valor de otro registro al registro de la izquierda
    def __init__(self, destino, fuente):
        self.destino = destino
        self.fuente = fuente
        
    def __str__(self):
        return f"<Mov {self.destino}, {self.fuente}>"

    def procesar(self, procesador):
        valor_fuente = procesador.get_registro(self.fuente)
        if valor_fuente is not None:
            procesador.set_registro(self.destino, valor_fuente)
        else:
            procesador.set_registro(self.destino, int(self.fuente))

class Add(Instruccion):
    # Suma dos registros o un registro y un valor literal y deja el resultado en el registro de la izquierda
    def __init__(self, destino, fuente):
        self.destino = destino
        self.fuente = fuente
        
    def __str__(self):
        return f"<Add {self.destino}, {self.fuente}>"

    def procesar(self, procesador):
        valor_fuente = procesador.get_registro(self.fuente)
        
        if valor_fuente is not None:
            procesador.set_registro(self.destino, procesador.get_registro(self.destino) + valor_fuente)
        else:
            procesador.set_registro(self.destino, procesador.get_registro(self.destino) + int(self.fuente))

class Jmp(Instruccion):
    # Saltar al lugar del programa que está referenciado por la etiqueta
    def __init__(self,ejecutable , etiqueta,):
        self.etiqueta = etiqueta
        self.ejecutable= ejecutable

    def __str__(self):
        return f"<Jmp {self.etiqueta}>"

    def procesar(self, procesador):
            direccion = self.ejecutable.lookupTable[self.etiqueta]
            procesador.cambiarIP(direccion)

class Jnz(Instruccion):
    # Saltar al lugar del programa que está referenciado por la etiqueta si el flag ZF 
    # esta en 0(si no pasa a la siguiente instrucción)
    
    def __init__(self, ejecutable, etiqueta):
        self.etiqueta = etiqueta
        self.ejecutable = ejecutable

    def __str__(self):
        return f"<Jnz {self.etiqueta}>"

    def procesar(self, procesador):
        if procesador.get_registro('ZF') == 0:
            direccion = self.ejecutable.lookupTable[self.etiqueta]
            procesador.cambiarIP(direccion)

class Jnc(Instruccion):
    # Saltar al lugar del programa que está referenciado por la etiqueta si el flag CF 
    # esta en 1(si no pasa a la siguiente instrucción)
    
    def __init__(self, ejecutable, etiqueta):
        self.etiqueta = etiqueta
        self.ejecutable = ejecutable

    def __str__(self):
        return f"<Jnz {self.etiqueta}>"

    def procesar(self, procesador):
        if procesador.get_registro('CF') == 1:
            direccion = self.ejecutable.lookupTable[self.etiqueta]
            procesador.cambiarIP(direccion)

class Cmp(Instruccion):
    def __init__(self, valor1, valor2):
        self.valor1 = valor1
        self.valor2 = valor2

    def __str__(self):
        return f"<Cmp {self.valor1}, {self.valor2}>"

    def procesar(self, procesador):
        
        if procesador.get_registro(self.valor1) is not None:
            valor1 = procesador.get_registro(self.valor1)
        else:
            valor1 = int(self.valor1)
        
        if procesador.get_registro(self.valor2) is not None:
            valor2 = procesador.get_registro(self.valor2)
        else:
            valor2 = int(self.valor2)

        if valor1 == valor2:
            procesador.set_registro('ZF', 1)
            procesador.set_registro('CF', 0)
        elif valor1 < valor2:
            procesador.set_registro('ZF', 0)
            procesador.set_registro('CF', 1)
        else:
            procesador.set_registro('ZF', 0)
            procesador.set_registro('CF', 0)

class Inc(Instruccion):
    # Incrementa en 1 el valor de un registro
    def __init__(self, registro):
        self.registro = registro
        
    def __str__(self):
        return f"<Inc {self.registro}>"

    def procesar(self, procesador):
        procesador.set_registro(self.registro, procesador.get_registro(self.registro) + 1)

class Dec(Instruccion):
    # Decrementa en 1 el valor de un registro
    def __init__(self, registro):
        self.registro = registro

    def __str__(self):
        return f"<Dec {self.registro}>"

    def procesar(self, procesador):
        procesador.set_registro(self.registro, procesador.get_registro(self.registro) - 1)
        
class Noop(Instruccion):
    # Incremeta en 1 la IP
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta

    def __str__(self):
        return f"<Noop {self.etiqueta}>"
        
    def procesar(self, procesador):
        pass


class Push(Instruccion):
    # Empuja un valor en la pila
    def __init__(self,ejecutable, valor):
        self.ejecutable = ejecutable
        self.valor = valor

    def __str__(self):
        return f"<Push {self.valor}>"

    def procesar(self, procesador):
        if self.valor.isdigit():  # Si el valor es un entero
            valor = int(self.valor)
        else:  # Si el valor es un registro
            valor = procesador.get_registro(self.valor)
        self.ejecutable.pila.append(valor)


class Pop(Instruccion):
    # Saca un valor de la pila y lo asigna a un registro
    def __init__(self,ejecutable, registro):
        self.ejecutable = ejecutable
        self.registro = registro

    def __str__(self):
        return f"<Pop {self.registro}>"

    def procesar(self,procesador):
        if self.ejecutable.pila:  # Verificar que la pila no esté vacía
            valor = self.ejecutable.pila.pop()
            procesador.set_registro(self.registro, valor)
        else:
            raise IndexError("La pila está vacía, no se puede sacar ningún elemento")
        
class Call(Instruccion):
    def __init__(self,ejecutable, etiqueta):
        self.ejecutable = ejecutable
        self.etiqueta = etiqueta

    def __str__(self):
        return f"<CALL {self.etiqueta}>"

    def procesar(self, procesador):
        direccion_retorno = procesador.get_registro('ip') + 1 # Dirección de retorno
        self.ejecutable.pila.append(direccion_retorno )  # Agregar al tope de la pila
        procesador.cambiarIP(self.ejecutable.lookupTable[self.etiqueta])  # Ir a la etiqueta

class Ret(Instruccion):
    def __init__(self,ejecutable):
        self.ejecutable = ejecutable
    
    def __str__(self):
        return "<RET>"

    def procesar(self, procesador): 
        direccion_retorno = self.ejecutable.pila.pop() # Obtener la dirección de retorno
        procesador.cambiarIP(direccion_retorno)  # Continuar desde la dirección de retorno

class Int(Instruccion):
    def __init__(self, nro):
        self.nro = int (nro)
        
    def __str__(self):
        return f"<Int {self.nro}>"

    def procesar(self, procesador):
        sisop = procesador.get_sisOp()
        parametros = []
        
        if self.nro == 1: 
            # en ax vamos a tener el entero que queremos imprimir, en bx tendrá la fila 
            # y cx la columna de donde donde quiero que se imprima en la pantalla
            parametros = [procesador.get_registro('ax'), procesador.get_registro('bx'), procesador.get_registro('cx')]
        else:
            # Error
            raise IndexError("Error de ejecucion: numero de servicio invalido")
        
        sisop.syscallHandler(self.nro, parametros)
        
class Neg(Instruccion):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"<Neg {self.valor}>"
    
    def procesar(self, procesador):
        valor = procesador.get_registro(self.valor)
        
        if valor is None:
            valor = - int(valor)
            procesador.set_registro('ax', valor)
        
        else:
            procesador.set_registro(self.valor, -valor)
        

class Jle(Instruccion):
    def __init__(self, ejecutable, etiqueta):
        self.etiqueta = etiqueta
        self.ejecutable = ejecutable

    def __str__(self):
        return f"<Jle {self.etiqueta}>"

    def procesar(self, procesador):
        if procesador.get_registro('ZF') == 1 or procesador.get_registro('CF') == 1:
            direccion = self.ejecutable.lookupTable[self.etiqueta]
            procesador.cambiarIP(direccion)

class Sub(Instruccion):
    # Resta el valor de fuente del destino y almacena el resultado en destino
    def __init__(self, destino, fuente):
        self.destino = destino
        self.fuente = fuente

    def __str__(self):
        return f"<Sub {self.destino}, {self.fuente}>"

    def procesar(self, procesador):
        valor_fuente = procesador.get_registro(self.fuente)
        if valor_fuente is not None:
            procesador.set_registro(self.destino, procesador.get_registro(self.destino) - valor_fuente)
        else:
            procesador.set_registro(self.destino, procesador.get_registro(self.destino) - int(self.fuente))

class ClearFlags(Instruccion):
    def __init__(self,ejecutable):
        self.ejecutable = ejecutable
        
    def __str__(self):
        return "<ClearFlags>"

    def procesar(self, procesador):
        procesador.set_registro('ZF', 0)
        procesador.set_registro('CF', 0)
