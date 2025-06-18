import os
import requests
import time
import json
import re
import concurrent.futures
import socket
from pathlib import Path
from datetime import datetime
import shutil

# ====== 텔레그램 알림 함수 ======
def send_telegram(msg):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not (token and chat_id): return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception:
        pass

# ====== ZeroDNS 파이프라인 전체 ======
def run_zerodns():
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
    DNS_TIMEOUT = 1.0
    MAX_WORKERS = 20
    INCLUDE_CATEGORIES = {3, 4, 6, 14, 15, 101}

    def log(msg):  # 경량 로깅
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def download(url, out_path):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            out_path.write_bytes(r.content)
            log(f"다운로드 완료: {url}")
        except Exception as e:
            log(f"다운로드 실패: {url} ({e})")

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

    t_start = time.time()
    WORK_DIR.mkdir(exist_ok=True)

    # 1. 소스 다운로드
    for url in FILTER_SOURCES:
        fname = url.split("/")[-1].split("?")[0]
        out_path = WORK_DIR / fname
        download(url, out_path)
    download(TRACKER_JSON_URL, TRACKERS_JSON_PATH)

    # 2. 필터 소스 병합 + 중복 + 1차 정제(루트만 남김)
    domains = set()
    pattern = re.compile(r"^\|\|([a-zA-Z0-9\-_.]+)\^$")
    for file in WORK_DIR.iterdir():
        if not file.is_file() or file.suffix not in [".txt", ".adblock"]:
            continue
        for line in file.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = pattern.match(line.strip())
            if m:
                dom = m.group(1)
                # ".." 포함, 비표준문자, 유니코드 제외
                if ".." in dom or re.search(r"[^\w\.\-]", dom):
                    continue
                domains.add(dom)
    # 루트 도메인만 남기고 서브 모두 제거
    roots = set(get_root(dom) for dom in domains)
    filtered = {dom for dom in domains if dom == get_root(dom)}
    log(f"1차 정제 완료: {len(filtered):,}개 (루트 도메인)")

    # 3. trackers.json 추출(카테고리 3,4,6,14,15,101)
    always_include = set()
    try:
        with open(TRACKERS_JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)
        trackers = data.get("trackers") or data
        for tracker in trackers.values():
            cat = tracker.get("category") or tracker.get("categoryId")
            dom = tracker.get("domain") or tracker.get("name")
            if isinstance(cat, str) and cat.isdigit():
                cat = int(cat)
            if cat in INCLUDE_CATEGORIES and dom and "." in dom:
                always_include.add(dom)
    except Exception as e:
        log(f"trackers.json 처리 오류: {e}")
    log(f"trackers.json 포함 도메인: {len(always_include):,}개")

    # 4. DNS 검사 제외 도메인(트래커) + 검사 대상 분리
    to_check = [dom for dom in filtered if dom not in always_include]
    final_domains = {dom for dom in filtered if dom in always_include}
    total = len(to_check)
    log(f"DNS 검사 대상 도메인: {total:,}개")

    # 5. 병렬 DNS 검사 + 진행률
    checked = set()
    count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_domain = {executor.submit(check_dns, dom): dom for dom in to_check}
        for future in concurrent.futures.as_completed(future_to_domain):
            dom = future_to_domain[future]
            count += 1
            if count % 100 == 0 or count == total:
                log(f"진행률: {count}/{total} ({count/total*100:.1f}%)")
            try:
                if future.result():
                    checked.add(dom)
            except Exception as e:
                log(f"DNS 검사 오류: {e}")

    ALL = final_domains | checked
    log(f"최종 줄 수: {len(ALL):,}개 (필터링/정제/검사 완료)")

    # 6. ZeroDNS.txt 출력
    with open("ZeroDNS.txt", "w", encoding="utf-8") as f:
        f.write("! ========== ZERODNS BLOCKLIST ==========\n")
        f.write("!      No Ads  |  No Stats  |  No Tracking\n")
        f.write("!   iOS·AdGuard 최적화 DNS 필터 | Aggressive & Precise\n")
        f.write(f"!   필터 줄 수: {len(ALL):,}개\n")
        f.write(f"!   마지막 업데이트: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
        f.write(f"!   광고/트래커 온리 도메인: {len(always_include):,}개 (DNS 검사 생략)\n")
        f.write(f"!   필터 소스:\n")
        for url in FILTER_SOURCES:
            f.write(f"!    - {url}\n")
        f.write(f"!   trackers.json: {TRACKER_JSON_URL}\n")
        f.write("! ========================================\n\n")
        for dom in sorted(ALL):
            f.write(f"||{dom}^\n")

    # 이전 결과(줄 수) 저장
    now = len(ALL)
    prev = 0
    try:
        with open("ZeroDNS.txt.prev", encoding="utf-8") as fp:
            prev = sum(1 for _ in fp)
    except Exception:
        pass
    shutil.copyfile("ZeroDNS.txt", "ZeroDNS.txt.prev")
    diff = now - prev
    duration = round(time.time() - t_start)
    return now, diff, duration

# ========== 메인 진입부 ==========
if __name__ == "__main__":
    t0 = time.time()
    try:
        now, diff, duration = run_zerodns()
        msg = (
            f"✅ *ZeroDNS 업데이트 완료!*\n"
            f"- 총 줄 수: `{now:,}`\n"
            f"- 증감: `{diff:+,}`\n"
            f"- 실행시간: `{duration // 60}분 {duration % 60}초`\n"
            f"- {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}"
        )
        send_telegram(msg)
    except Exception as e:
        duration = round(time.time() - t0)
        msg = (
            f"❌ *ZeroDNS 실패!*\n"
            f"- 에러: `{e}`\n"
            f"- 실행시간: `{duration // 60}분 {duration % 60}초`\n"
            f"- {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}"
        )
        send_telegram(msg)
        raise
