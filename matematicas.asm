multiplicar:
    push dx
    mov dx, 0
    mov dx, ax
    mov ax, 0
    
    loop_mul:
    add ax, bx
    dec dx
    cmp dx, 0
    jnz loop_mul
    pop dx
    clearflags
    ret

division:
    push dx
    mov dx, 0
    mov dx, ax
    mov ax, 0
    
    loop_div:
    cmp dx, bx
    jnc loop_div_end
    sub dx, bx
    inc ax
    jmp loop_div
    
    loop_div_end:
    pop dx
    clearflags
    ret

raizcuadrada:
    push dx
    mov dx, ax
    mov ax, 1
    
    push bx
    mov bx, 1

    loop_raiz:
    call multiplicar  
    cmp dx, ax
    jle fin_raiz           
    inc bx
    mov ax, bx          
    jmp loop_raiz   

    fin_raiz:
    mov ax, bx
    pop bx          
    pop dx
    clearflags       
    ret

potencia2:
    cmp ax, 0
    push bx
    jnz potencia_negativa

    potencia_base:
    mov bx, ax
    call multiplicar
    jmp potencia_final

    potencia_negativa:
    clearflags
    neg ax
    mov bx, ax
    call multiplicar
    jmp potencia_final

    potencia_final:
    pop bx
    ret
