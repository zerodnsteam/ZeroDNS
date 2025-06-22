import random
from datetime import datetime

def get_random_message(status, line_count, stats, errors, raw_total):
    today = datetime.now().strftime("%Y-%m-%d")
    line_text = f"{line_count:,}줄"

    # 성공 바이브
    success_vibes = [
        f"💖 ZeroDNS 오늘도 조용히 다 정리했어요.\n누군가한테 도움이 되었으면 좋겠어요 🫧\n"
        f"📅 {today}  📄 {line_text}",
        f"🌸 오늘도 무사히 끝! 혼자서 정리해봤어요.\n필터 적용 끝! 💗\n"
        f"📅 {today}  📄 {line_text}",
        f"🫧 ZeroDNS 필터 업데이트 완료.\n오늘은 조금 덜 힘들었어요…\n"
        f"📅 {today}  📄 {line_text}",
        f"🍀 혼자서 다 했어요. 조금 힘들긴 했지만, 그래도 성공!\n고마워요 💚\n"
        f"📅 {today}  📄 {line_text}",
    ]

    # 실패 바이브
    fail_vibes = [
        f"💔 ZeroDNS 실패… 이번엔 오류가 있어서 멈췄어요.\n그래도 다음엔 더 잘할게요 🥲\n"
        f"📅 {today}  📄 {line_text}",
        f"😢 오늘은 정리가 안 됐어요… 미안해요\n"
        f"📅 {today}  📄 {line_text}",
        f"🪻 ZeroDNS 실패… 왜인지 모르겠지만 조금 속상해요\n"
        f"📅 {today}  📄 {line_text}",
    ]

    if status == "success":
        return random.choice(success_vibes)
    else:
        return random.choice(fail_vibes)
