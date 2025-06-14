from datetime import datetime
from pathlib import Path

# === 1. 필터 원본 파일 목록 (필요하면 추가/삭제) ===
filter_dir = Path("filters")
input_files = [
    "native.apple.txt",
    "ultimate.mini.txt",
    "adblock.txt",
    "oisd_small.txt",
    "filter_25.txt",
    "filter_1_ios.txt"
]
input_paths = [filter_dir / f for f in input_files]
output_path = Path("ZeroDNS.txt")

# === 2. 도메인 집합(중복 제거) 만들기 ===
domains = set()
for file in input_paths:
    if not file.exists():
        print(f"Warning: {file} 없음 (스킵)")
        continue
    for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("||") and line.endswith("^"):
            domains.add(line)

# === 3. 헤더 주석 (아스키아트 + 줄 수/날짜/정보 자동화) ===
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
    "!   · Hagezi native.apple",
    "!   · Hagezi ultimate.mini",
    "!   · 1Hosts Lite",
    "!   · oisd small",
    "!   · AdGuard HostlistsRegistry #25",
    "!   · AdGuard DNS filter (iOS)",
    "! Maintainer : zerodnsteam | https://github.com/zerodnsteam/ZeroDNS",
    "! ==========================================================",
    ""
]

# === 4. 파일로 출력 ===
with output_path.open("w", encoding="utf-8") as f:
    f.write('\n'.join(ascii_logo))
    for d in sorted(domains):
        f.write(d + "\n")

print(f"ZeroDNS 병합 완료! 도메인 개수: {len(domains):,}개")
