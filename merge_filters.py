from datetime import datetime
from pathlib import Path

filter_dir = Path("filters")
input_files = [
    "native.apple.txt",
    "ultimate.txt",              
    "1hosts-Xtra_adblock.txt",   
    "oisd_big.txt",              
    "filter_25.txt",
    "filter_1_ios.txt"
]
input_paths = [filter_dir / f for f in input_files]
output_path = Path("ZeroDNS.txt")

domains = set()
for file in input_paths:
    if not file.exists():
        print(f"Warning: {file} 없음 (스킵)")
        continue
    for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("||") and line.endswith("^"):
            domains.add(line)

ascii_logo = [
    "! ███████╗███████╗██████╗  ██████╗ ██████╗ ███╗   ██╗███████╗",
    "! ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔══██╗████╗  ██║██╔════╝",
    "!   ███╔╝ █████╗  ██████╔╝██║   ██║██║  ██║██╔██╗ ██║███████╗",
    "!  ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║  ██║██║╚██╗██║╚════██║",
    "! ███████╗███████╗██║  ██║╚██████╔╝██████╔╝██║ ╚████║███████║",
    "! ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝",
    "! ==========================================================",
    "! ZeroDNS : 중복 제거 · 자동 병합 · iOS AdGuard 최적화",
    f"! 최신 업데이트 : {datetime.now().strftime('%Y-%m-%d %H:%M %z')}",
    f"! 총 도메인 수  : {len(domains):,}",
    "! [소스]",
    "!   · hagezi native.apple",
    "!   · hagezi ultimate",
    "!   · 1hosts Xtra",
    "!   · oisd big",
    "!   · AdGuard HostlistsRegistry #25",
    "!   · AdGuard DNS filter (iOS)",
    "! Maintainer : zerodnsteam | https://github.com/zerodnsteam/ZeroDNS",
    "! ==========================================================",
    ""
]

with output_path.open("w", encoding="utf-8") as f:
    f.write('\n'.join(ascii_logo))
    for d in sorted(domains):
        f.write(d + "\n")

print(f"ZeroDNS 병합 완료! 도메인 개수: {len(domains):,}개")
