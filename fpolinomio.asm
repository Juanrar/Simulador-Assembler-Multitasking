include "matematicas.asm"

fpolinomio:
    mov dx, ax

    ;4ac----------------------
    push bx
    mov bx, cx
    call multiplicar 
    mov bx, 4
    call multiplicar
    mov cx, ax

    ;b**2---------------------  
    pop ax
    push ax
    call potencia2

    ;b**2 - 4ac---------------
    neg cx
    add ax, cx

    ;raiz---------------------
    call raizcuadrada
    mov cx, ax

    ; -b
    pop bx
    neg bx

    ; ax =-b + resultado_raiz------
    add ax, bx

    ; cx = -b - resultado_raiz------
    neg cx
    add cx, bx

    ; 2a
    add dx, dx

    ; divisiones
    mov bx, dx
    call division
    push ax

    mov ax, cx
    call division

    ; Las raíces se almacenarán en AX y BX
    pop bx
    ret