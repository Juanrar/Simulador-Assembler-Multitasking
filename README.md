# Simulador de Ensamblador en Python

Este proyecto es un simulador de ensamblador escrito en Python que incluye implementaciones de varias funciones matemáticas en lenguaje ensamblador, como la multiplicación, división, cálculo de raíz cuadrada y la secuencia de Fibonacci.

## Descripción

El simulador de ensamblador permite la ejecución de instrucciones básicas de ensamblador utilizando una máquina virtual simple en Python. El proyecto incluye las siguientes características:

- **Instrucciones básicas**: `MOV`, `ADD`, `JMP`, `JNZ`, `CMP`, `INC`, `DEC`, `NOOP`, `PUSH`, `POP`, `CALL`, `RET`, `INT`, `NEG`
- **Funciones matemáticas**:
  - **Multiplicación**: Implementada utilizando sumas sucesivas.
  - **División**: Implementada utilizando restas sucesivas.
  - **Raíz cuadrada**: Implementada utilizando un método de aproximación por pruebas.
  - **Fibonacci**: Implementada utilizando un enfoque recursivo.

A partir de la lectura de un archivo de codigo assembler, se lo ensambla y se crea un ejetuable. Se emula la funcion de un procesador, sistema operativo, system calls y includes.
