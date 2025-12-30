import re
from pathlib import Path

# ====== CONFIG ======
ROOT = r"E:\水果派\2025_12"   # <- change this
DRY_RUN = False             # True = only print, False = actually rename
# ====================

RX = re.compile(r"^(?!水果派)\d{6}")

def needs_prefix(name: str) -> bool:
    return RX.match(name) is not None

def with_conflict_suffix(dst: Path) -> Path:
    """If dst exists, create dst__1, dst__2 ... (keeps multi-suffix like .tar.gz)."""
    if not dst.exists():
        return dst

    suffixes = "".join(dst.suffixes)          # e.g. ".tar.gz"
    base = dst.name[:-len(suffixes)] if suffixes else dst.name

    for i in range(1, 10_000):
        cand = dst.with_name(f"{base}__{i}{suffixes}")
        if not cand.exists():
            return cand
    raise RuntimeError(f"Too many conflicts for: {dst}")

root = Path(ROOT).expanduser().resolve()
if not root.is_dir():
    raise SystemExit(f"Not a folder: {root}")

for p in root.rglob("*"):
    if not p.is_file():
        continue

    if needs_prefix(p.name):
        dst = p.with_name("水果派" + p.name)
        dst = with_conflict_suffix(dst)

        print(f"{p}  ->  {dst}")
        if not DRY_RUN:
            p.rename(dst)
print("Done.")