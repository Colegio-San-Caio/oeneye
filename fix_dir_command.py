with open("emu.py", "r") as f:
    content = f.read()

# Old hardcoded DIR block to replace
old_block = """elif cmd == "DIR":
    target_dir = DRIVE_MAPPINGS.get(current_drive, ".")
    if os.path.isdir(target_dir):
        items = os.listdir(target_dir)
    print(f"1 file(s)  {os.path.getsize(target_dir)} bytes")"""

# New FAT12-aware DIR block
new_block = """elif cmd == "DIR":
    target_img = DRIVE_MAPPINGS.get(current_drive, "oeneye.img")
    try:
        with open(target_img, "rb") as f_img:
            img_data = f_img.read()
        cmd_dir(img_data)
    except Exception as e:
        # Fallback to directory listing if not a raw image
        target_dir = target_img
        if os.path.isdir(target_dir):
            items = os.listdir(target_dir)
            print(f" Directory of {target_dir}\\\\n")
            for item in items:
                print(f"{item:<12}")
            print(f"\\n {len(items)} File(s)\\n")
        else:
            print(f"1 file(s)  {os.path.getsize(target_dir)} bytes")"""

if old_block.strip() in content:
    content = content.replace(old_block.strip(), new_block)
    with open("emu.py", "w") as f:
        f.write(content)
    print("Successfully updated DIR command in emu.py!")
else:
    print("Could not find exact block, appending cmd_dir handler manually.")
    # Append the cmd_dir function definition if not present
    if "def cmd_dir" not in content:
        content += "\n" + """
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
        with open("emu.py", "w") as f:
            f.write(content)
        print("Appended cmd_dir definition.")
