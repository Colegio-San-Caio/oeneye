bits 16
org 0x8000
start:
  cli
  xor ax, ax
  mov ds, ax
  mov es, ax
  mov ss, ax
  mov sp, 0x7C00
  sti
  cld
  mov si, msg
  call print
pl:
  mov si, prompt
  call print
  mov di, buf
  xor cx, cx
key:
  xor ah, ah
  int 16h
  cmp al, 13
  je enter
  cmp al, 8
  je bksp
  cmp al, 32
  jb key
  cmp al, 126
  ja key
  cmp cx, 30
  jae key
  stosb
  inc cx
  call putc
  jmp key
bksp:
  test cx, cx
  jz key
  dec di
  dec cx
  mov al, 8
  call putc
  mov al, 32
  call putc
  mov al, 8
  call putc
  jmp key
enter:
  xor al, al
  stosb
  mov si, crlf
  call print
  test cx, cx
  jz pl
  mov si, buf
  mov di, c_help
  call streq
  jc do_help
  mov si, buf
  mov di, c_ver
  call streq
  jc do_ver
  mov si, buf
  mov di, c_clear
  call streq
  jc do_clear
  mov si, buf
  mov di, c_quit
  call streq
  jc do_quit
  mov si, unk
  call print
  jmp pl
do_help:
  mov si, helptxt
  call print
  jmp pl
do_ver:
  mov si, vertxt
  call print
  jmp pl
do_clear:
  mov ax, 0003h
  int 10h
  jmp pl
do_quit:
  mov dx, 0x604
  mov ax, 0x2000
  out dx, ax
  mov dx, 0xB004
  out dx, ax
  mov si, haltmsg
  call print
  jmp $
streq:
  push si
  push di
.l:
  lodsb
  mov ah, [di]
  inc di
  cmp al, ah
  jne .no
  test al, al
  jnz .l
  pop di
  pop si
  stc
  ret
.no:
  pop di
  pop si
  clc
  ret
putc:
  mov ah, 0Eh
  xor bx, bx
  int 10h
  ret
print:
  lodsb
  or al, al
  jz .d
  call putc
  jmp print
.d:
  ret
msg db 'oeneyeOS Stage2 - Active [0x8000] - B: 2.88M OK',13,10,'Type help for commands',13,10,0
prompt db '> ',0
helptxt db 'help  ver  clear  quit',13,10,0
vertxt db 'oeneyeOS v1.0 Stage2',13,10,0
unk db 'unknown command',13,10,0
crlf db 13,10,0
c_help db 'help',0
c_ver db 'ver',0
c_clear db 'clear',0
c_quit db 'quit',0
haltmsg db 'power-off unsupported - CTRL+A then X',13,10,0
buf times 32 db 0
times 1024-($-$$) db 0
