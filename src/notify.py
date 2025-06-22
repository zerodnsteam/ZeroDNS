import requests, os

def send_telegram(msg, logger):
    try:
        token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        if not token or not chat_id:
            raise RuntimeError("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID 시크릿이 누락됨")
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": msg}
        r = requests.post(url, data=data, timeout=20)
        logger.log(f"  → 텔레그램 전송 결과: {r.status_code}")
    except Exception as e:
        logger.log(f"  → 텔레그램 전송 실패: {e}")
