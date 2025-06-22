import random
from datetime import datetime

SUCCESS_VIBES = [
    "🩵 ZeroDNS 필터 정리 완료했어요!\n오늘도 조용히, 깔끔하게 끝냈어요. 누군가에게 도움이 되길 바랄게요 💫",
    "🌱 혼자서 조용히 정리했어요. 조금 힘들긴 했지만… 그래도 잘 마무리했어요.",
    "🫧 다 정리했어요… 작지만 누군가에겐 도움이 되면 좋겠어요.",
]

SUCCESS_WITH_WARNINGS_VIBES = [
    "🌸 ZeroDNS 필터는 잘 완성했어요!\n근데 몇몇 도메인 줄이 이상했어요 😅",
    "🟡 필터 적용엔 성공! 그런데 형식이 이상한 줄이 조금 있었어요. 큰 문제는 아니에요 💛",
]

FAIL_VIBES = [
    "💔 ZeroDNS 실패… 이번엔 오류가 있어서 멈췄어요. 조금 속상해요 🥲",
    "😞 필터 만들다가 중간에 멈췄어요. 다시 시도해볼게요...",
]

NOCHANGE_VIBES = [
    "🕊️ ZeroDNS는 오늘 조용히 지나갔어요.\n업데이트된 도메인이 없어서, 그대로 유지할게요.",
    "😶 변화가 없어서 오늘은 아무 작업도 하지 않았어요.",
]

def get_random_message(status, lines, stats, errors):
    today = datetime.now().strftime("%Y-%m-%d")

    # 필터 통계 요약
    total_sources = len(stats) if stats else 0
    original_total = sum(stat.get('original_lines', 0) for stat in stats.values()) if stats else 0

    # 상태별 메시지
    if status == "success":
        msg = random.choice(SUCCESS_VIBES)
    elif status == "success_with_warnings":
        msg = random.choice(SUCCESS_WITH_WARNINGS_VIBES)
        if errors:
            msg += f"\n\n⚠️ 이상하거나 읽기 어려운 도메인 줄이 {len(errors):,}개 있었어요\n→ output/parse_errors.txt에 저장했어요!"
    elif status == "fail":
        msg = random.choice(FAIL_VIBES)
        if errors:
            msg += f"\n\n🔍 오류 예시: {errors[0][:120]}"
    else:
        msg = random.choice(NOCHANGE_VIBES)

    # 요약 정보 추가
    if total_sources and original_total:
        msg += f"\n\n📊 총 {total_sources}개 소스 처리 ({original_total:,}줄 → {lines:,}줄)"

    msg += f"\n📅 {today}  📄 최종 {lines:,}줄"
    return msg
