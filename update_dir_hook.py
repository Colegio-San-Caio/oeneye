with open("emu.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('elif cmd == "DIR":'):
        # Replace this whole block until the next elif/else/end of loop
        new_lines.append('elif cmd == "DIR":\n')
        new_lines.append('    target_img = DRIVE_MAPPINGS.get(current_drive, "oeneye.img")\n')
        new_lines.append('    try:\n')
        new_lines.append('        with open(target_img, "rb") as f_img:\n')
        new_lines.append('            img_data = f_img.read()\n')
        new_lines.append('        cmd_dir(img_data)\n')
        new_lines.append('    except Exception as e:\n')
        new_lines.append('        print(f"Error reading drive image: {e}")\n')
        
        # Skip the old hardcoded lines until the next elif or blank line block
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("elif") and not lines[i].strip().startswith("else") and lines[i].strip() != "":
            i += 1
        continue
    else:
        new_lines.append(line)
    i += 1

with open("emu.py", "w") as f:
    f.writelines(new_lines)

print("Successfully hooked cmd_dir into emu.py command loop!")
