from instruccion import Mov,Add,Jmp,Jnz,Cmp,Inc,Dec,Noop,Pop,Push,Call,Ret,Instruccion

class Mul(Instruccion):
    def __init__(self, destino, fuente):
        self.destino = destino
        self.fuente = fuente

    def __str__(self):
        return f"<Mul {self.destino}, {self.fuente}>"

    def procesar(self, procesador):
        valor_fuente = procesador.get_registro(self.fuente)
        
        if valor_fuente is not None:
            for _ in range(1,valor_fuente):
                add_temporal = Add(self.destino, valor_fuente)
                add_temporal.procesar(procesador)
                
        elif valor_fuente == 0 or int(self.fuente) == 0:
            cero = Mov(self.destino, 0)
            cero.procesar(procesador)
            
        else:
            for _ in range(1,int(self.fuente)):
                add_temporal = Add(self.destino, int(self.fuente))
                add_temporal.procesar(procesador)

class Div(Instruccion):
    def __init__(self, numerador, denominador):
        self.numerador = numerador
        self.denominador = denominador

    def __str__(self):
        return f"<Div {self.numerador}, {self.denominador}>"

    def procesar(self, procesador):
        valor_numerador = procesador.get_registro(self.numerador)
        valor_denominador = procesador.get_registro(self.denominador)
        
        if valor_denominador is None:
            valor_denominador = int(self.denominador)
        
        if valor_denominador == 0:
            raise ValueError("Division por cero")
        
        cociente = 0
        suma = 0
        
        while suma + valor_denominador <= valor_numerador:
            suma += valor_denominador
            cociente += 1
        
        if (valor_numerador < 0 and valor_denominador > 0) or (valor_numerador > 0 and valor_denominador < 0):
            cociente = -cociente
        
        resto = valor_numerador - (cociente * valor_denominador)

        procesador.set_registro(self.numerador, cociente)  # Guardar cociente en el registro del numerador
        procesador.set_registro(self.denominador, resto if resto != 0 else valor_denominador)   # Guardar resto en el registro del denominador

class Rzc(Instruccion):
    def __init__(self, valor):
        self.valor = valor
    
    def __str__(self):
        return f"<Rzc {self.valor}>"
    
    def procesar(self, procesador):
        numero = procesador.get_registro(self.valor)
        
        if numero is None:
            numero = int(self.valor)
        
        if numero < 0:
            raise ValueError("El valor no puede ser negativo")
        
        elif numero == 0:
            procesador.set_registro('ax', 0)
        
        estimacion = 1
        while estimacion * estimacion <= numero:
            estimacion += 1
        
        procesador.set_registro('ax',estimacion - 1)

class Fcd(Instruccion):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
    def __init__(self):
        return f"<Fcd {self.a},{self.b},{self.c}>"
    
    def procesar(self, procesador):
        # Calcular el discriminante
        discriminante = self.b**2 - 4*self.a*self.c
        
        # Caso cuando el discriminante es negativo(raices complejas)
        if discriminante < 0:
            pass
        
        # Caso cuando el discriminante es cero (una raiz real)
        elif discriminante == 0:
            pass
        
        # Caso cuando el discriminante es positivo(dos raices reales)
        else:
            pass
 
class Fib(Instruccion):
    def __init__(self,valor ):
        self.valor = valor
    
    def __str__(self):
        return f"<Fic {self.valor}>"
    
    def procesar(self, procesador):
        numero = procesador.get_registro(self.valor)
        
        if numero is None:
            numero = int(self.valor)
            
        if numero <= 0:
            raise ValueError("El valor debe ser mayor a cero")
        
        elif numero == 1:
            procesador.set_registro('ax', 1)
        
        elif numero == 2:
            procesador.set_registro('ax', 1)
        
        else:
            #return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)
            fib1 = Fib(numero - 1)
            fib1.procesar(procesador)
            resultado = procesador.get_registro('ax')
            
            fib2 = Fib(numero - 2)
            fib2.procesar(procesador)
            resultado += procesador.get_registro('ax')
            
            procesador.set_registro('ax', resultado)