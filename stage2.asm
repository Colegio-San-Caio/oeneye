[bits 16]
[org 0x8000]
mov si, msg
call print
hlt
jmp $
print: lodsb
or al, al
jz.r
mov ah, 0x0E
int 0x10
jmp print
.r: ret
msg db 'oeneyeOS Stage2 - Active [0x8000] - B: 2.88M OK',13,10,0
times 1024-($-$$) db 0
