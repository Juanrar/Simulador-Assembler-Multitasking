fibonacci:
    ;base if n <= 1, return n
    cmp ax, 1
    jle end_fibonacci

    ;fibonacci(n-1)
    push ax
    sub ax, 1
    call fibonacci
    pop bx
    push ax

    ;fibonacci(n-2)
    sub bx, 2
    mov ax, bx
    call fibonacci
    
    ;fibonacci(n - 1) + fibonacci(n - 2)
    pop bx
    add ax, bx

end_fibonacci:
    ret

