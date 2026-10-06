#!/usr/bin/env python3
import pathlib

root = pathlib.Path(".")
out = root / "CATALOG.md"

# Match any subfolder containing a README.md (excluding root)
books = sorted([p for p in root.glob("**/README.md") if p != root / "README.md"])

with open(out, "w", encoding="utf-8") as f:
    f.write("# OenEye - Catalog (auto)\n\n")
    for md in books:
        f.write(f"\n## {md.parent.name}\n\n")
        f.write(md.read_text(encoding="utf-8", errors="ignore")[:4000])
        f.write("\n\n---\n")

print(f"[cat] wrote {out} from {len(books)} files")
