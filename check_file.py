import re
from pathlib import Path
from collections import defaultdict, Counter

# ====== CONFIG ======
ROOT = r"E:\水果派\水果派2025_11"   # 改成你的目录
OUT_FILE = "missing_names.txt"   # output filename under ROOT
WRITE_PREFIX_FORM = True         # also write "水果派{date}{label}_"
# ====================

# 匹配：可选前缀“水果派”，6位日期，连续字母(至少1位)，下划线
RX = re.compile(r'^(?:水果派)?(\d{6})([A-Za-z]+)_')

def label_to_num(label: str) -> int:
    """Excel-like: A=1, B=2, ..., Z=26, AA=27 ..."""
    label = label.upper()
    n = 0
    for ch in label:
        if not ('A' <= ch <= 'Z'):
            raise ValueError(f"Invalid label: {label}")
        n = n * 26 + (ord(ch) - ord('A') + 1)
    return n

def num_to_label(n: int) -> str:
    """1->A, 2->B, 26->Z, 27->AA ..."""
    if n <= 0:
        raise ValueError("n must be >= 1")
    out = []
    while n > 0:
        n, r = divmod(n - 1, 26)
        out.append(chr(ord('A') + r))
    return "".join(reversed(out))

root = Path(ROOT).expanduser().resolve()
if not root.is_dir():
    raise SystemExit(f"Not a folder: {root}")

# date -> list of label strings
date_labels = defaultdict(list)

for p in root.rglob("*"):
    if not p.is_file():
        continue
    m = RX.match(p.name)
    if not m:
        continue
    date = m.group(1)
    label = m.group(2).upper()
    date_labels[date].append(label)

missing_all = []  # collect missing names to write

# 输出报告（按日期排序）
for date in sorted(date_labels.keys()):
    labels = date_labels[date]
    c = Counter(labels)

    # 转数字（用于连续性判断）
    nums = []
    bad = []
    for lb in labels:
        try:
            nums.append(label_to_num(lb))
        except ValueError:
            bad.append(lb)

    if bad:
        print(f"[{date}] WARNING: invalid labels: {sorted(set(bad))}")

    if not nums:
        print(f"[{date}] no valid items")
        continue

    min_n = min(nums)
    max_n = max(nums)

    # 你说“first is A”，所以从 A(=1) 开始检查到 last
    start_n = 1
    present = set(nums)
    missing = [num_to_label(i) for i in range(start_n, max_n + 1) if i not in present]

    duplicates = [lb for lb, cnt in c.items() if cnt > 1]
    duplicates.sort(key=lambda x: label_to_num(x))

    first_label = num_to_label(min_n)
    last_label = num_to_label(max_n)

    print(f"[{date}] count={len(labels)}  first={first_label}  last={last_label}")
    if missing:
        print(f"  missing({len(missing)}): {', '.join(missing)}")
    else:
        print("  missing: (none)")
    if duplicates:
        print(f"  duplicates({len(duplicates)}): {', '.join(duplicates)}")

    # ===== collect missing names =====
    for lb in missing:
        # 原始缺失名
        add_filename = f"{date}{lb}"
        if WRITE_PREFIX_FORM:
            add_filename = f"水果派{add_filename}_"
        missing_all.append(add_filename)

        # 额外：I -> 1，O -> 0
        if lb == "I":
            add2 = f"{date}1"
            if WRITE_PREFIX_FORM:
                add2 = f"水果派{add2}_"
            missing_all.append(add2)
        elif lb == "O":
            add2 = f"{date}0"
            if WRITE_PREFIX_FORM:
                add2 = f"水果派{add2}_"
            missing_all.append(add2)

# ===== write to file =====
# out_path = root / OUT_FILE
out_path = OUT_FILE
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(missing_all))

print(f"\nSaved missing names to: {out_path}")