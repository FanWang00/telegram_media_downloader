import os
from pathlib import Path



def transform_name(name: str) -> str:
    # replace anywhere in the name
    return name.replace("1_", "I_").replace("0_", "O_")

def unique_target(dst: Path) -> Path:
    """If dst exists, append ' (n)' to avoid collisions."""
    if not dst.exists():
        return dst

    parent = dst.parent
    stem = dst.stem
    suffix = dst.suffix  # '' for folders

    i = 1
    while True:
        cand = parent / (f"{stem} ({i}){suffix}" if suffix else f"{dst.name} ({i})")
        if not cand.exists():
            return cand
        i += 1

def rename_recursively(root: Path) -> int:
    root = root.resolve()
    changes = 0

    # bottom-up so directory renames don't break traversal
    for dirpath, dirnames, filenames in os.walk(root, topdown=False, followlinks=FOLLOW_SYMLINKS):
        dirpath = Path(dirpath)

        # rename files
        for fname in filenames:
            new_name = transform_name(fname)
            if new_name == fname:
                continue
            src = dirpath / fname
            dst = unique_target(dirpath / new_name)
            print(f"[FILE] {src}  ->  {dst}")
            changes += 1
            if not DRY_RUN:
                src.rename(dst)

        # rename directories
        for dname in dirnames:
            new_name = transform_name(dname)
            if new_name == dname:
                continue
            src = dirpath / dname
            dst = unique_target(dirpath / new_name)
            print(f"[DIR ] {src}  ->  {dst}")
            changes += 1
            if not DRY_RUN:
                src.rename(dst)

    return changes


if __name__ == "__main__":
    
    
    ROOT = r"E:\水果派\水果派2025_11"   # <-- change this
    DRY_RUN = False              # True = preview only, False = actually rename
    FOLLOW_SYMLINKS = False
    total = rename_recursively(Path(ROOT))
    print(f"\nDone. {'Planned' if DRY_RUN else 'Renamed'}: {total}")
