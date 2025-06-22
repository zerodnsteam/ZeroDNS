import requests, json

def send_telegram(msg, logger):
    try:
        with open("settings.json", encoding="utf-8") as f:
            conf = json.load(f)
        url = f"https://api.telegram.org/bot{conf['bot_token']}/sendMessage"
        data = {"chat_id": conf['chat_id'], "text": msg}
        r = requests.post(url, data=data, timeout=20)
        logger.log(f"  → 텔레그램 전송 결과: {r.status_code}")
    except Exception as e:
        logger.log(f"  → 텔레그램 전송 실패: {e}")
