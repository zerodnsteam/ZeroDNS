import requests
import os

def send_telegram(message: str, logger=None):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        if logger:
            logger.warning("텔레그램 토큰 또는 챗 ID 없음")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, data={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    })

    if logger:
        logger.info(f"텔레그램 전송 결과: {resp.status_code}")
