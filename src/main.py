from vibes import get_random_message
from notify import send_telegram
from datetime import datetime

# 필터 도메인 개수, 오류 리스트, 필터별 통계, 다운로드 소스 사전
line_count = final_line_count      # 필터 최종 줄 수
errors = parse_errors              # 도메인 파싱 중 이상한 줄
sources = source_files             # {OISD: ..., HAGEZI: ..., ...}

# 실패/성공/경고 구분
CRITICAL_FAIL = (
    line_count == 0 or
    any(v is None for v in sources.values())
)
PARSING_ERROR_RATIO = len(errors) / max(line_count, 1)

if CRITICAL_FAIL:
    status = "fail"
elif PARSING_ERROR_RATIO > 0.05:
    status = "fail"
elif len(errors) > 0:
    status = "success_with_warnings"
else:
    status = "success"

# 감정 멘트 + 알림 전송
msg = get_random_message(status, line_count, filter_stats, errors)
send_telegram(msg, logger)
