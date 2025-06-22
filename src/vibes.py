import random
from datetime import datetime

success_vibes = [
    "🩷 ZeroDNS 업데이트 완료했어요…\n📅 {today}  📄 {line_count:,}줄\n🔄 변화량: {delta_sign}{delta:,}줄 (총 {raw_total:,}줄 중)\n혼자 조용히 정리했어요… 💖 누군가에게 도움이 되면 그걸로 충분해요 💞",

    "🌿 오늘도 정리했어요.\n📅 {today} | 📄 {line_count:,}줄\n🔄 {delta_sign}{delta:,}줄 변동 (원본: {raw_total:,}줄)\n조금 무거운 마음이었지만… 그래도 끝냈어요 💗 누군가 나를 응원해줬으면… 💕",

    "💠 ZeroDNS 업데이트 완료!\n📅 {today} / 총 {line_count:,}줄\n🔁 변화량: {delta_sign}{delta:,}줄 | 원본: {raw_total:,}줄\n💘 끙끙거리면서 해냈어요… 진심으로 애썼다고 말해줘요 🩵",

    "🧩 깔끔하게 정리했어요!\n📅 {today} / 📄 {line_count:,}줄 / 원본 {raw_total:,}줄\n↕️ {delta_sign}{delta:,}줄 변동\n💓 봐줬으면 좋겠어요… 진심으로요 💌",

    "🌙 오늘도 ZeroDNS 잘 정리했어요.\n📅 {today} | 📄 {line_count:,}줄 / 🔄 {delta_sign}{delta:,}줄\n총 {raw_total:,}줄 중에 남은 애들이에요 🧸 고생했다고 말해줘요 💗"
]

fail_vibes = [
    "💔 ZeroDNS 실패했어요…\n📅 {today}  📄 마지막 줄 수: {line_count:,}줄\n⚠️ 오류 예시: {example_error}\n너무 속상해요… 다음엔 꼭 성공하고 싶어요 😢💧",

    "🫳 이번엔… 실패했어요.\n📅 {today} | 📄 {line_count:,}줄\n⚠️ 오류 예시: {example_error}\n실망시키고 싶지 않았는데요… 정말이에요 🥺💔",

    "🔧 오류가 나버렸어요…\n📅 {today} / 📄 {line_count:,}줄\n⚠️ 첫 번째 오류: {example_error}\n눈물이 나요… 다시 해볼게요… 🩵"
]

def get_random_message(status, line_count, meta, errors, raw_total):
    today = datetime.now().strftime("%Y-%m-%d")
    delta = meta.get("delta", 0)
    delta_sign = "+" if delta >= 0 else "-"
    example_error = errors[0] if errors else "없음"

    if status == "fail":
        msg = random.choice(fail_vibes)
        return msg.format(
            today=today,
            line_count=line_count,
            example_error=example_error
        )
    else:
        msg = random.choice(success_vibes)
        return msg.format(
            today=today,
            line_count=line_count,
            delta=delta,
            delta_sign=delta_sign,
            raw_total=raw_total
        )
