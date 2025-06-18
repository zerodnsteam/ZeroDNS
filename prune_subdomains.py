from pathlib import Path

input_path = Path("ZeroDNS_resolved.txt")
output_path = Path("ZeroDNS.txt")

def get_root(domain):
    parts = domain.split('.')
    if len(parts) < 2:
        return domain
    return '.'.join(parts[-2:])

with input_path.open("r", encoding="utf-8") as f:
    domains = [line.strip() for line in f if line.strip() and line.startswith("||") and line.endswith("^")]

roots = set(get_root(d[2:-1]) for d in domains)
final_domains = set()
for d in domains:
    dom = d[2:-1]
    if get_root(dom) == dom or get_root(dom) not in roots:
        final_domains.add(d)

header = [
    "! Title: ZeroDNS",
    "! Description: iOS·AdGuard에 최적화된 매우 공격적인 DNS 필터",
    "! Version: 2025.06.17",
    "! Last modified: 2025-06-17T00:00:00Z",
    "! Expires: 1 day",
    "! Homepage: https://github.com/zerodnsteam/ZeroDNS",
    "! ========== ZERODNS BLOCKLIST ==========",
    "!      No Ads  |  No Stats  |  No Tracking",
    "!   iOS·AdGuard 최적화 DNS 필터 | Aggressive & Precise",
    "! Source: Hagezi / 1Hosts / OISD / AdGuard / List-KR",
    "! Maintainer: zerodnsteam",
    "! ========================================"
]

with output_path.open("w", encoding="utf-8") as f:
    for line in header:
        f.write(line + "\n")
    for d in sorted(final_domains):
        f.write(d + "\n")

print(f"ZeroDNS 최종 필터 생성 완료! ({len(final_domains):,}개)")
