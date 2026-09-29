with open("emu.py", "r") as f:
    content = f.read()

# Clean up any misplaced top-level elif
content = content.replace("elif cmd == \"DIR\":\n    target_img", "    elif cmd == \"DIR\":\n        target_img")

with open("emu.py", "w") as f:
    f.write(content)

print("Syntax corrected!")
