import logging
from datetime import datetime
from parser import parse_domains
from notify import send_telegram
from vibes import get_random_message
import subprocess

# ===== 로거 설정 =====
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ===== (예시) 필터 소스 파일 딕셔너리 =====
sources = {
    "OISD": "filters/OISD.txt",
    "HAGEZI_ULTIMATE": "filters/HAGEZI_ULTIMATE.txt",
    "HAGEZI_NATIVE-APPLE": "filters/HAGEZI_NATIVE-APPLE.txt",
    "1HOSTS_PRO": "filters/1HOSTS_PRO.txt",
    "LIST-KR": "filters/LIST-KR.txt",
    "ADGUARD_DNS": "filters/ADGUARD_DNS.txt"
}

# ===== [1] 도메인 파싱 및 정제 =====
domains, errors, raw_total = parse_domains(sources, logger)
line_count = len(domains)

# ===== [2] 필터 저장 (AdGuard 스타일) =====
out_fn = "output/ZeroDNS.txt"
with open(out_fn, "w", encoding="utf-8") as f:
    for d in sorted(domains):
        f.write(f"||{d}^\n")
logger.info(f"필터 저장 완료: {out_fn} ({line_count:,}줄)")

# ===== [3] 상태 판단 (실패/경고/성공/변화없음) =====
CRITICAL_FAIL = (line_count == 0 or any(v is None for v in sources.values()))
PARSING_ERROR_RATIO = len(errors) / max(line_count, 1)
if CRITICAL_FAIL:
    status = "fail"
elif PARSING_ERROR_RATIO > 0.05:
    status = "fail"
elif len(errors) > 0:
    status = "success_with_warnings"
else:
    status = "success"

# ===== [4] 텔레그램 알림 =====
msg = get_random_message(status, line_count, {}, errors, raw_total)
send_telegram(msg, logger)

# ===== [5] GitHub 자동 커밋/푸시 =====
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

logger.info(f"전체 작업 완료! (최종 라인 수: {line_count:,})")
logger.info(f"GitHub에 필터 자동 푸시 중…")
git_commit_and_push(out_fn, logger)
