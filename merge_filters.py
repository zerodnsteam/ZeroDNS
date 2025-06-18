from pathlib import Path

filter_dir = Path("filters")
input_files = [
    "native.apple.txt",
    "ultimate.txt",
    "adblock.txt",
    "oisd_big.txt",
    "filter_25.txt",
    "filter_1_ios.txt"
]
input_paths = [filter_dir / f for f in input_files]
output_path = Path("ZeroDNS_raw.txt")

def valid_domain(line):
    if not (line.startswith("||") and line.endswith("^")):
        return False
    d = line[2:-1]
    if '..' in d:
        return False
    try:
        d.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

domains = set()
for file in input_paths:
    if not file.exists():
        print(f"Warning: {file} 없음 (스킵)")
        continue
    for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if valid_domain(line):
            domains.add(line)

with output_path.open("w", encoding="utf-8") as f:
    for d in sorted(domains):
        f.write(d + "\n")

print(f"ZeroDNS 병합/정제 완료! 도메인 개수: {len(domains):,}개")
