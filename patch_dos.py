import os

# Ensure configuration / rc startup script for oeneyeOS v0.2
rc_content = """@ECHO OFF
PROMPT A:\\>
PATH A:\\;A:\\BIN
SET OS=oeneyeOS
SET AGI_TOKEN=000b
VER
"""

with open("oeneye.rc", "w") as f:
    f.write(rc_content)

print("[SUCCESS] oeneye.rc startup configuration generated.")
