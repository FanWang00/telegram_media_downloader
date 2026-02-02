import os
import re
from pathlib import Path



def transform_name(name: str) -> str:
    # Replace 1/0 only in patterns like: <date><token>_
    # where <date> is digits and <token> is letters or 1/0
    pattern = re.compile(r"(\d+)([A-Za-z10]+)_")

    def repl(match: re.Match) -> str:
        date_part = match.group(1)
        token = match.group(2).replace("1", "I").replace("0", "O")
        return f"{date_part}{token}_"

    return pattern.sub(repl, name)

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
    
    
    ROOT = r"C:\Users\wf\Documents\GitHub\telegram_media_downloader\downloads\水果派🍉AV解说福利社\2026_02"
    DRY_RUN = False              # True = preview only, False = actually rename
    FOLLOW_SYMLINKS = False
    total = rename_recursively(Path(ROOT))
    print(f"\nDone. {'Planned' if DRY_RUN else 'Renamed'}: {total}")
