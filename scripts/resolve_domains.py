import os
import json
import re
import concurrent.futures
import socket
import requests
from pathlib import Path

# ========== 설정 ==========
FILTER_SOURCES = [
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@main/adblock/native.apple.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@main/adblock/ultimate.txt",
    "https://cdn.jsdelivr.net/gh/badmojr/1Hosts@master/Pro/adblock.txt",
    "https://cdn.jsdelivr.net/gh/sjhgvr/oisd@main/oisd_big.txt",
    "https://cdn.jsdelivr.net/gh/adguardteam/HostlistsRegistry@main/assets/filter_25.txt",
    "https://filters.adtidy.org/dns/filter_1_ios.txt"
]
TRACKER_JSON_URL = "https://cdn.jsdelivr.net/gh/AdguardTeam/companiesdb@main/dist/trackers.json"
WORK_DIR = Path("filters")
TRACKERS_JSON_PATH = WORK_DIR / "trackers.json"

DNS_SERVERS = [
    "1.1.1.1", "8.8.8.8", "76.76.2.0", "208.67.222.222"
]
DNS_TIMEOUT = 1.5
MAX_WORKERS = 15

def download(url, out_path):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        out_path.write_bytes(r.content)
        print(f"다운로드 완료: {url}")
    except Exception as e:
        print(f"[!] 다운로드 실패: {url} ({e})")

def get_root(domain):
    parts = domain.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain

def check_dns(domain):
    try:
        for server in DNS_SERVERS:
            try:
                socket.setdefaulttimeout(DNS_TIMEOUT)
                socket.gethostbyname_ex(domain)
                return True
            except Exception:
                continue
        return False
    except Exception:
        return False

def main():
    WORK_DIR.mkdir(exist_ok=True)
    # 1. 소스/트래커DB 다운로드
    for url in FILTER_SOURCES:
        fname = url.split("/")[-1].split("?")[0]
        out_path = WORK_DIR / fname
        download(url, out_path)
    download(TRACKER_JSON_URL, TRACKERS_JSON_PATH)

    # 2. 광고/트래커 도메인 추출
    always_include = set()
    try:
        with open(TRACKERS_JSON_PATH, encoding="utf-8") as f:
            trackers = json.load(f)["trackers"]
        for tracker in trackers.values():
            cat = tracker.get("category")
            dom = tracker.get("domain")
            if cat in (3, 4, 6, 15) and dom:
                always_include.add(dom)
        print(f"광고/트래커 도메인: {len(always_include)}개")
    except Exception as e:
        print(f"[!] trackers.json 처리 에러: {e}")

    # 3. 필터 병합/정제
    domains = set()
    pattern = re.compile(r"^\|\|([a-zA-Z0-9\-_.]+)\^$")
    for file in WORK_DIR.iterdir():
        if not file.is_file() or file.suffix not in [".txt", ".adblock"]:
            continue
        for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = pattern.match(line.strip())
            if m:
                dom = m.group(1)
                if ".." in dom or re.search(r"[^\w\.\-]", dom):
                    continue
                domains.add(dom)

    # 4. 광고/트래커 우선 포함
    final_domains = set()
    for dom in domains:
        root = get_root(dom)
        if dom in always_include or root in always_include:
            final_domains.add(dom)

    # 5. 나머지 도메인 DNS 검사(병렬)
    to_check = [dom for dom in domains if dom not in always_include and get_root(dom) not in always_include]
    checked = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_domain = {executor.submit(check_dns, dom): dom for dom in to_check}
        for future in concurrent.futures.as_completed(future_to_domain):
            dom = future_to_domain[future]
            try:
                if future.result():
                    checked.add(dom)
            except Exception:
                pass

    ALL = final_domains | checked

    # 6. 서브도메인 정제(루트 있으면 서브 제거)
    roots = set(get_root(dom) for dom in ALL)
    ALL = {dom for dom in ALL if dom == get_root(dom) or get_root(dom) not in roots - {dom}}

    # 7. 최종 출력
    with open("ZeroDNS.txt", "w", encoding="utf-8") as f:
        f.write("! ========== ZERODNS BLOCKLIST ==========\n")
        f.write("!      No Ads  |  No Stats  |  No Tracking\n")
        f.write("!   iOS·AdGuard 최적화 DNS 필터 | Aggressive & Precise\n")
        f.write(f"!   필터 줄 수: {len(ALL):,}개\n")
        f.write(f"!   마지막 업데이트: {os.popen('date -u').read().strip()} UTC\n")
        f.write(f"!   광고/트래커 온리 도메인: {len(always_include):,}개 (DNS 검사 생략)\n")
        f.write(f"!   필터 소스:\n")
        for url in FILTER_SOURCES:
            f.write(f"!    - {url}\n")
        f.write(f"!   trackers.json: {TRACKER_JSON_URL}\n")
        f.write("! ========================================\n\n")
        for dom in sorted(ALL):
            f.write(f"||{dom}^\n")

    print(f"ZeroDNS.txt 생성 완료! 최종 줄 수: {len(ALL):,}개")

if __name__ == "__main__":
    main()
