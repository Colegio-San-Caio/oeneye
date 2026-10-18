; hexdiff_DBoqm.asm - (0)b Evergreen / No Date - JP DEV
; DOS.COM - hex diff with OQM BUS0 JC canary
; nasm -f bin hexdiff_DBoqm.asm -o hexdiff_DBoqm.com
org 100h
    jmp start
msg1 db 'hexdiff_DBoqm (0)b Evergreen$'
msg2 db 13,10,'FILE1: NASMusbOQM_OMQ.com old$'
msg3 db 13,10,'FILE2: NASMusbOQM_OMQ.com new$'
msgdiff db 13,10,'DIFF at $'
msgarrow db ' : $'
msgok db 13,10,'OQM OMQ: BUS0 OK - canary closed$'
msgfail db 13,10,'OQM FAIL JC (0)b$'
hexchr db '0123456789ABCDEF'

start:
    mov ah,09h
    mov dx,msg1
    int 21h
    mov dx,msg2
    int 21h
    mov dx,msg3
    int 21h

    ; simple hex dump of first 64 bytes of our own COM to show (0)b logic
    mov si,100h
    mov cx,64
.dump:
    push cx
    mov al,[si]
    ; high nibble
    mov bl,al
    shr al,4
    call print_hex
    mov al,bl
    and al,0Fh
    call print_hex
    mov dl,' '
    mov ah,02h
    int 21h
    ; JC test = BUS0 error canary
    jc fail
    inc si
    pop cx
    loop.dump

    mov ah,09h
    mov dx,msgok
    int 21h
    int 20h
fail:
    mov ah,09h
    mov dx,msgfail
    int 21h
    int 20h

print_hex:
    push bx
    mov bx,hexchr
    xlat
    mov dl,al
    mov ah,02h
    int 21h
    pop bx
    ret
