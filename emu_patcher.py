import sys

content = ""
with open("emu.py", "r") as f:
    content = f.read()

# 1. Check if MOUNT logic already exists
if "elif cmd == \"MOUNT\":" in content:
    print("[INFO] emu.py already patched. Skipping.")
    sys.exit(0)

# 2. Define mount block
mount_block = """
        elif cmd == \\"MOUNT\\":
            if len(parts) >= 3:
                target_drv = parts[1].rstrip(\\":\\").upper()
                img_file = parts[2].strip()
                if target_drv in DRIVE_MAPPINGS:
                    DRIVE_MAPPINGS[target_drv] = img_file
                    print(f"Drive {target_drv}: successfully mounted to {img_file}")
                else:
                    print(f"Invalid drive specifier: {target_drv}")
            else:
                print("Syntax error. Usage: MOUNT <drive>: <image>")
        elif cmd == \\"UNMOUNT\\":
            if len(parts) >= 2:
                target_drv = parts[1].rstrip(\\":\\").upper()
                if target_drv in DRIVE_MAPPINGS:
                    DRIVE_MAPPINGS[target_drv] = \\"\\"
                    print(f"Drive {target_drv}: unmounted.")
                else:
                    print(f"Invalid drive specifier: {target_drv}")
            else:
                print("Syntax error. Usage: UNMOUNT <drive>:")
"""

# 3. Inject block before the final else:
insertion_point = "else:\\n            print(f\\"Bad command or file name: {cmd}\\")"
content = content.replace(insertion_point, mount_block + "\\n        " + insertion_point)

with open("emu.py", "w") as f:
    f.write(content)
print("[SUCCESS] emu.py patched.")
