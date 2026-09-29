import os

sdk_dirs = [
    "workspace/sdk_v23/include",
    "workspace/sdk_v23/lib",
    "workspace/sdk_v23/bin",
    "workspace/sdk_v23/docs"
]

for d in sdk_dirs:
    os.makedirs(d, exist_ok=True)

# Create a sample v23 SDK header stub
header_content = """/*
 * MOSFETQ DOS SDK v23 Header
 * Target Runtime: v22 / v21NT
 * Floppy Core Dependency: v0.2 (Pinned & Locked)
 */

#ifndef MOSFETQ_SDK_V23_H
#define MOSFETQ_SDK_V23_H

#define MOS_API_VERSION 23
#define KERNEL_FLOPPY_VERSION "v0.2"

void* mos_alloc_virtual_drive(char drive_letter);
int mos_register_nt_subsystem(void);

#endif
"""

with open("workspace/sdk_v23/include/mos_sdk.h", "w") as f:
    f.write(header_content)

print("SDK v23 workspace scaffolded successfully in workspace/sdk_v23/!")
