import os
import logging
from datetime import datetime
import requests
import subprocess
from parser import parse_domains
from notify import send_telegram
from vibes import get_random_message

# ===== 로거 설정 =====
logger = logging.getLogger("ZeroDNS")
logging.basicConfig(level=logging.INFO)

# ===== [1/7] 필터 소스 URL 딕셔너리 =====
FILTER_SOURCES = {
    "OISD": "https://raw.githubusercontent.com/cbuijs/oisd/master/big/domains",
    "HAGEZI_ULTIMATE": "https://raw.githubusercontent.com/cbuijs/hagezi/main/lists/ultimate/domains",
    "HAGEZI_NATIVE-APPLE": "https://raw.githubusercontent.com/cbuijs/hagezi/main/lists/native-apple/domains",
    "1HOSTS_PRO": "https://raw.githubusercontent.com/cbuijs/1hosts/main/Pro/domains",
    "LIST-KR": "https://cdn.jsdelivr.net/gh/adguardteam/HostlistsRegistry@main/assets/filter_25.txt",
    "ADGUARD_DNS": "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt"
}
FILTERS_DIR = "filters"

def download_sources(sources, logger):
    os.makedirs(FILTERS_DIR, exist_ok=True)
    for name, url in sources.items():
        outpath = os.path.join(FILTERS_DIR, f"{name}.txt")
        logger.info(f"[1/7]   - {name} 다운로드 중…")
        try:
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            with open(outpath, "w", encoding="utf-8") as f:
                f.write(resp.text)
            logger.info(f"[1/7]     성공: {outpath} ({len(resp.text.splitlines()):,}줄)")
        except Exception as e:
            logger.warning(f"[1/7]     실패: {name} ({e})")

download_sources(FILTER_SOURCES, logger)

sources = {name: f"{FILTERS_DIR}/{name}.txt" for name in FILTER_SOURCES}

# ===== [2/7] 도메인 파싱 및 정제 =====
domains, errors, raw_total = parse_domains(sources, logger)
line_count = len(domains)

# ===== [3/7] 필터 저장 (AdGuard 스타일) =====
os.makedirs("output", exist_ok=True)
out_fn = "output/ZeroDNS.txt"
with open(out_fn, "w", encoding="utf-8") as f:
    for d in sorted(domains):
        f.write(f"||{d}^\n")
logger.info(f"[4/7] 필터 저장 완료: {out_fn} ({line_count:,}줄)")

# ===== [4/7] 상태 판단 (실패/경고/성공/변화없음) =====
CRITICAL_FAIL = (line_count == 0 or any(not os.path.isfile(fn) for fn in sources.values()))
PARSING_ERROR_RATIO = len(errors) / max(line_count, 1)
if CRITICAL_FAIL:
    status = "fail"
elif PARSING_ERROR_RATIO > 0.05:
    status = "fail"
elif len(errors) > 0:
    status = "success_with_warnings"
else:
    status = "success"

# ===== [5/7] 텔레그램 알림 =====
msg = get_random_message(status, line_count, {}, errors, raw_total)
send_telegram(msg, logger)

# ===== [6/7] GitHub 자동 커밋/푸시 =====
def git_commit_and_push(file_path: str, logger=None):
    try:
        subprocess.run(["git", "config", "--global", "user.name", "zerodns-bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"🔄 ZeroDNS 필터 업데이트 ({datetime.now().strftime('%Y-%m-%d')})"], check=True)
        subprocess.run(["git", "push"], check=True)
        if logger:
            logger.info(f"✅ Git push 성공: {file_path}")
    except subprocess.CalledProcessError as e:
        if logger:
            logger.error(f"❌ Git push 실패: {e}")

logger.info(f"[7/7] 전체 작업 완료! (최종 라인 수: {line_count:,})")
logger.info(f"[7/7] GitHub에 필터 자동 푸시 중…")
git_commit_and_push(out_fn, logger)
