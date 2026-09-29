with open("emu.py", "r") as f:
    content = f.read()

new_dir_func = """
def cmd_dir(img_data, bps=512, root_lba=19, root_entries=224):
    print(" Volume in drive A has no label.")
    print(" Directory of A:\\\\n")
    
    root_offset = root_lba * bps
    entry_size = 32
    file_count = 0
    total_bytes = 0
    
    for i in range(root_entries):
        entry_offset = root_offset + (i * entry_size)
        entry = img_data[entry_offset : entry_offset + entry_size]
        
        first_byte = entry[0]
        if first_byte == 0x00:
            break
        if first_byte == 0xE5:
            continue
            
        attr = entry[11]
        if attr == 0x0F:
            continue
            
        name = entry[0:8].decode('ascii', errors='ignore').strip()
        ext = entry[8:11].decode('ascii', errors='ignore').strip()
        filename = f"{name}.{ext}" if ext else name
        
        fsize = int.from_bytes(entry[28:32], byteorder='little')
        
        if attr & 0x10:
            print(f"{filename:<12}   <DIR>")
        else:
            print(f"{filename:<12} {fsize:>10} bytes")
            total_bytes += fsize
        file_count += 1
        
    print(f"\\n {file_count} File(s) {total_bytes} bytes free\\n")
"""

# Replace existing cmd_dir or append it
if "def cmd_dir" in content:
    # Find and replace the function roughly or append a new override
    print("Found existing cmd_dir function.")
else:
    content += "\n" + new_dir_func
    with open("emu.py", "w") as f:
        f.write(content)
    print("Appended new DIR parser to emu.py!")
