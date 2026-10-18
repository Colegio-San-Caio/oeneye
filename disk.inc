; Read sectors using BIOS INT 13h
; Inputs: DL = drive number, DH = head, CH = cylinder, CL = sector, AL = sector count, ES:BX = destination buffer
disk_load:
    push dx             ; Save DX for later comparison
    mov ah, 0x02        ; BIOS read sector function
    int 0x13            ; Call BIOS disk service
    jc disk_error       ; Jump if carry flag set (error)
    pop dx
    cmp al, dh          ; Compare sectors read with expected count
    jne sector_error
    ret

disk_error:
    mov si, msg_disk_err
    call print_string
    jmp $

sector_error:
    mov si, msg_sect_err
    call print_string
    jmp $

msg_disk_err db 'Disk read error!', 0x0d, 0x0a, 0
msg_sect_err db 'Sector read mismatch!', 0x0d, 0x0a, 0
