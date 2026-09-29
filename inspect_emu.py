with open("emu.py", "r") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "DIR" in line or "dir" in line or "command" in line.lower():
        print(f"{idx+1}: {line.strip()}")
