from datetime import datetime
from vibes import get_random_message
from notify import send_telegram
import subprocess
import logging

# ===== 로거 설정 =====
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ===== 사전 변수 (예시) =====
line_count = 526355  # 최종 필터 줄 수
parse_errors = ["1HOSTS PRO:88:09_19.supfree.net"]  # 예시 오류 줄
source_files = {
    "OISD": "filters/OISD.txt",
    "HAGEZI_ULTIMATE": "filters/HAGEZI_ULTIMATE.txt",
    "HAGEZI_NATIVE-APPLE": "filters/HAGEZI_NATIVE-APPLE.txt",
    "1HOSTS_PRO": "filters/1HOSTS_PRO.txt",
    "LIST-KR": "filters/LIST-KR.txt",
    "ADGUARD_DNS": "filters/ADGUARD_DNS.txt"
}
filter_stats = {
    name: {"original_lines": sum(1 for _ in open(path, encoding='utf-8'))}
    for name, path in source_files.items()
}

# ===== 상태 판단 =====
CRITICAL_FAIL = (
    line_count == 0 or
    any(v is None for v in source_files.values())
)
PARSING_ERROR_RATIO = len(parse_errors) / max(line_count, 1)

if CRITICAL_FAIL:
    status = "fail"
elif PARSING_ERROR_RATIO > 0.05:
    status = "fail"
elif len(parse_errors) > 0:
    status = "success_with_warnings"
else:
    status = "success"

# ===== 텔레그램 메시지 전송 =====
msg = get_random_message(status, line_count, filter_stats, parse_errors)
send_telegram(msg, logger)

# ===== GitHub 자동 커밋/푸시 =====
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

logger.info(f"[7/7] 전체 작업 완료! (라인 수: {line_count:,})")
logger.info(f"[8/7] GitHub에 필터 자동 푸시 중…")
git_commit_and_push("output/ZeroDNS.txt", logger)
