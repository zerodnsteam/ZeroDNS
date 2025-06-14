from pathlib import Path

filter_dir = Path("filters")
output_file = Path("ZeroDNS.txt")
domains = set()

for file in filter_dir.glob("*.txt"):
    for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("||") and line.endswith("^"):
            domains.add(line)

with output_file.open("w", encoding="utf-8") as f:
    for d in sorted(domains):
        f.write(d + "\n")

print(f"Merged {len(domains)} domains to {output_file}")
