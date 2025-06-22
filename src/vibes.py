import random
from datetime import datetime

SUCCESS_VIBES = [
    "🫧 ZeroDNS 필터 정리 끝! 오늘은 조용히 정리만 했어요. 도움이 됐으면 좋겠어요 💗",
    "✅ 필터 갱신 완료!… 그냥 살짝 힘들었지만 괜찮아요 🫥",
    "🌿 오늘도 잘 마무리했어요. 누군가에게 도움이 되면 좋겠네요 🪽"
]
FAIL_VIBES = [
    "💔 ZeroDNS 실패… 이번엔 오류가 있어서 멈췄어요. 조금 속상해요 🥲",
    "🪫 필터 처리하다 에러… 저도 멘탈 나갔어요 😵‍💫",
    "😢 오늘은 잘 안 됐네요. 에러 로그 확인 부탁드려요 🫠"
]
NOCHANGE_VIBES = [
    "🫥 오늘은 변화 없었어요. 그래도 무탈하니 다행이죠? 🤍",
    "☁️ ZeroDNS 그대로예요. 고요한 하루… 🍃"
]

def get_random_message(status, lines, stats, errors):
    today = datetime.now().strftime("%Y-%m-%d")
    if status == "success":
        msg = random.choice(SUCCESS_VIBES)
    elif status == "fail":
        msg = random.choice(FAIL_VIBES)
        if errors:
            msg += f"\n\n🔍 오류 예시: {errors[0][:120]}"
    else:
        msg = random.choice(NOCHANGE_VIBES)
    msg += f"\n📅 {today}  📄 {lines:,}줄"
    return msg
