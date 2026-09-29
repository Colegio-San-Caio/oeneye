import os
import sys
import subprocess
import shutil
import datetime
import glob

def get_all_drive_mappings():
    mappings = {
        "A": "floppy_img.bin",
        "C": ".",
        "W": "workspace",
        "X": "shared_storage"
    }
    files = sorted(glob.glob("*.img") + glob.glob("*.zip") + glob.glob("*.tar*") + glob.glob("*.gz"))
    available_letters = [chr(c) for c in range(ord('D'), ord('Z')+1) if chr(c) not in mappings]
    
    for f_path, letter in zip(files, available_letters):
        mappings[letter] = f_path
    return mappings

DRIVE_MAPPINGS = get_all_drive_mappings()

def run_backup():
    if os.path.exists("backup.py"):
        print("Running automatic session backup...")
        subprocess.run(["python3", "backup.py"], capture_output=True, text=True)

def main():
    global current_path, current_drive
    current_drive = "A"
    current_path = "A:\\"
    
    print("Checking for repository updates...")
    try:
        subprocess.run(["git", "pull"], capture_output=True, text=True, timeout=3)
    except Exception:
        pass

    print("Loading MOSFETQ DOS v19...")
    print("\nMOSFETQ DOS v19.0 (ARM64 Optimized)")
    print("Type HELP for a list of commands.")

    while True:
        try:
            user_input = input(f"{current_drive}:\\> ")
        except (KeyboardInterrupt, EOFError):
            break

        raw = user_input.strip()
        upper_raw = raw.upper()

        if len(upper_raw) == 2 and upper_raw[1] == ":" and upper_raw[0] in DRIVE_MAPPINGS:
            current_drive = upper_raw[0]
            current_path = current_drive + ":\\"
            target = DRIVE_MAPPINGS[current_drive]
            if os.path.isdir(target) or target == ".":
                os.makedirs(target, exist_ok=True)
            print(f"Current drive: {current_drive}")
            continue

        if upper_raw == "BACKUP":
            run_backup()
            continue

        if upper_raw == "EXIT":
            run_backup()
            print("Exiting MOSFETQ DOS...")
            break

        parts = raw.split()
        if not parts:
            continue
        
        cmd = parts[0].upper()
        if cmd == "HELP":
            print("Available commands: DIR, TREE, MAP, CD <dir>, CLS, EXIT, BACKUP")
        elif cmd == "MAP":
            print("Active Drive Mappings:")
            for drv, path in DRIVE_MAPPINGS.items():
                if os.path.exists(path):
                    print(f"  {drv}: -> {path}")
        elif cmd == "DIR":
            target_dir = DRIVE_MAPPINGS.get(current_drive, ".")
            if os.path.isfile(target_dir):
                print(f"Volume in drive {current_drive} has no label.")
                print(f"Directory of {current_drive}:\\\n")
                print(f"1 file(s)     {os.path.getsize(target_dir)} bytes")
            elif os.path.isdir(target_dir):
                print(f"Volume in drive {current_drive} has no label.")
                print(f"Directory of {current_drive}:\\\n")
                items = os.listdir(target_dir)
                for item in items:
                    print(f"               {item}")
                print(f"\nTotal files listed:\n {len(items)} item(s)")
            else:
                print("Directory not found.")
        elif cmd == "CLS":
            os.system("cls" if os.name == "nt" else "clear")
        else:
            target_dir = DRIVE_MAPPINGS.get(current_drive, ".")
            possible_file = os.path.join(target_dir, raw)
            if os.path.isfile(possible_file) and raw.endswith(".py"):
                print(f"Executing {raw}...")
                subprocess.run(["python3", possible_file])
            else:
                print(f"Bad command or file name: {raw}")

if __name__ == "__main__":
    main()
