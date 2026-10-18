; 0hEomqPasswd_BIN - AH=0Ah + JC + (0)b binary
org 100h
mov dx, msg
mov ah, 09h
int 21h

mov dx, buf     ; AH=0Ah buffered input
mov ah, 0Ah
int 21h
jc  fail        ; JC = (0)b carry if error / Ctrl-C

; (0)b mode = binary, no CR/LF translate
; check len
mov al, [buf+1]
or al, al
jz fail

; success - save to 0hEomqPasswd_BIN
mov dx, ok_msg
mov ah, 09h
int 21h
ret

fail:
mov dx, err_msg
mov ah, 09h
int 21h
ret

msg db '0hE Passwd: $'
ok_msg db 13,10,'0hE OK$'
err_msg db 13,10,'0hE FAIL JC$'
buf db 64,0,64 dup(0)
