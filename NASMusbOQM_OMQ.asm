; NASMusbOQM_OMQ.asm - USB BUS (b)0 OQM canary
; org 100h DOS .COM - AH=0Ah passwd + USB BUS 0 enum
; License: GPL-3.0 - original Oeneye, no MSC code
org 100h

; --- 0hE passwd prompt AH=09h
mov dx, msg_0hE
mov ah, 09h
int 21h

; --- AH=0Ah buffered, (0)b binary, JC check
mov dx, buf
mov ah, 0Ah
int 21h
jc  fail_bus

mov al, [buf+1]
or al, al
jz fail_bus

; --- USB (b)0 BUS 0 simulation - OMQ grid
mov dx, msg_usb
mov ah, 09h
int 21h

; Here you'd map USB endpoints -> NASTRAN GRIDs
; GRID 0 = BUS0 DEV0, GRID 1 = ENDP0 control
; For now just show OK
mov dx, msg_ok
mov ah, 09h
int 21h
ret

fail_bus:
mov dx, msg_fail
mov ah, 09h
int 21h
ret

msg_0hE db '0hEomq Passwd: $'
msg_usb db 13,10,'NASMusb OQM BUS(b)0: enumerating...$'
msg_ok  db 13,10,'OQM OMQ: BUS0 OK - canary loop closed$'
msg_fail db 13,10,'OQM FAIL JC (0)b$'
buf db 64,0,64 dup(0)
