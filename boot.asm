org 0x7c00
mov ah,0x09
mov al,'7' ; your 7
mov bh,0
mov bl,0x0F
mov cx,1
int 0x10
jc err ; JC 0A -> if carry, error
jmp $
err: mov al,'!'
int 0x10
jmp $
times 510-($-$$) db 0
dw 0xAA55
