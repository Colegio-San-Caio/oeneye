import os, shutil, mimetypes
from datetime import datetime

TARGET_MIMES = {"application/octet-stream", "application/x-msdos-program"}

def log_event(msg, td):
    log_path = os.path.join(td, "orchestrator.log")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except:
        pass
    print(msg)

def parse_os_and_version(fn):
    fn_l = fn.lower()
    if "oeneye" in fn_l:
        return "oeneyeOS", "raw"
    if "date" in fn_l:
        return "date.img", "raw"
    if "data" in fn_l:
        return "data.img", "raw"
    return "Extracted_productions", "v1"

def categorize_by_version(td):
    for fn in list(os.listdir(td)):
        vp = os.path.join(td, fn)
        if not os.path.isfile(vp):
            continue
        if fn.lower().endswith((".py", ".log", ".sh", ".ddc", ".gnd")):
            continue
        try:
            mt, _ = mimetypes.guess_type(fn)
            if mt in TARGET_MIMES or fn.endswith((".xml", ".html", ".img", ".bin", ".dat")):
                ost, ver = parse_os_and_version(fn)
                dd = os.path.join(td, ost, ver)
                os.makedirs(dd, exist_ok=True)
                dest = os.path.join(dd, fn)
                if vp != dest:
                    shutil.move(vp, dest)
                    log_event(f"Moved: {fn} -> {ost}/{ver}", td)
        except Exception as e:
            print(f"Err: {e}")

def generate_ddc_registry(td):
    ddc_path = os.path.join(td, "orchestrator.ddc")
    try:
        with open(ddc_path, "w", encoding="utf-8") as fo:
            fo.write("[DDC_CONTROL_SPEC]\n")
            fo.write(f"timestamp={datetime.now().isoformat()}\n")
            fo.write(f"target_dir={td}\n")
            for root, dirs, files in os.walk(td):
                for f in files:
                    fo.write(f"{os.path.join(root, f)}\n")
        log_event(f"DDC registry written: {ddc_path}", td)
    except Exception as e:
        print(f"DDC Err: {e}")

if __name__ == "__main__":
    TARGET_DIR = "/storage/emulated/0/Download"
    log_event("=== RUNNING MAIN SUITE EXECUTION ===", TARGET_DIR)
    categorize_by_version(TARGET_DIR)
    generate_ddc_registry(TARGET_DIR)
    log_event("=== SUITE EXECUTION FINISHED OVER TIME ===", TARGET_DIR)
