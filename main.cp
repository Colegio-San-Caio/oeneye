# OQM OMQ - BUS0 Rules - Evergreen No Date
# main.cp - root copy-protection rules - DO NOT nano .BIN files

# RULE 1: Never nano binary
# .BIN .bin .COM .com are BINARY 263 bytes - use cp, never nano/vim
# text = .m .sh .sty .asm .cp .cpp -> nano OK
# binary = .BIN .COM -> ONLY cp / hexdump -C / strings

# RULE 2: Good size
# GOOD: 263 bytes
# BAD: 0 bytes, 2 lines, 3 lines = you nano'd it
# check: ls -lh santberk/MAIN.BIN ~/oeneye/MAIN.BIN
# check: strings santberk/MAIN.BIN | grep OQM

# RULE 3: cp restore - the only fix
# rm -f MAIN.BIN main.bin
# cp santberk/MAIN.BIN santberk/main.bin
# cp santberk/MAIN.BIN ~/oeneye/MAIN.BIN
# ls -lh santberk/MAIN.BIN ~/oeneye/MAIN.BIN # both 263

# RULE 4: Opcodes - your 7:26 PM dump
# B4 09 = MOV AH,09h = DOS print $ string / CD 21 = INT 21h
# 72 16 = JC +22 = opcode 0x72 Jump if Carry -> OQM FAIL JC (0)b$
# 73 cb = JNC = opcode 0x73 Jump if NOT Carry -> BUS0 OK
# 74 0F = JZ
# 73 as ASCII = 's' in "Password: $" = 50 61 73 73...

# RULE 5: Canary strings must exist in MAIN.BIN
# FILE1: NASMusbOQM_OMQ.com old$
# FILE2: NASMusbOQM_OMQ.com new$
# OQM OMQ: BUS0 OK - canary closed$
# OQM FAIL JC (0)b$0123456789ABCDEF

# RULE 6: Verification - 7:20 PM 22% good state
# hexdump -C santberk/MAIN.BIN | head
# BA 2E 01 B4 09 CD 21 BA 9F 01 B4 0A CD 21 72 16
# strings santberk/MAIN.BIN | grep OQM

# RULE 7: Git
# Good commit = 850f866 = 263b MAIN.BIN
# If git diff shows 0b or 3 lines -> rm + cp restore, don't push text

# FINAL: 7:26 PM 23% - both 263 bytes = good - STOP editing santberk/
# OQM OMQ: BUS0 OK - canary loop closed - no diff 225 bytes
