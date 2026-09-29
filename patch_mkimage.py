with open("mkimage.py", "r") as f:
    code = f.read()

# Check if OMQ.FNT is already added
if "OMQ.FNT" not in code:
    # Look for where files are added and inject OMQ.FNT
    target = 'add_files(('
    # Let's add it right before the file packing list or alongside docs/readme
    print("Patching mkimage.py to include OMQ.FNT...")
    
    # We can read OMQ.FNT from assets/fonts/ and add it to the file list dictionary
    font_addition = '''
# --- Include OMQ.FNT from local assets ---
try:
    with open("assets/fonts/OMQ.FNT", "rb") as ff:
        font_bytes = ff.read()
    # Add to files list for FAT12 injection
    files["OMQ.FNT"] = (0, len(font_bytes), font_bytes) # Note: handled via custom layout or add_files
except FileNotFoundError:
    print("Warning: assets/fonts/OMQ.FNT not found, skipping build injection.")
'''
    # Alternatively, append logic to inject it into the root/subdirectory layout
    with open("mkimage.py", "a") as f_out:
        f_out.write(font_addition)
    print("Patch appended successfully.")
else:
    print("mkimage.py already contains OMQ.FNT logic.")
