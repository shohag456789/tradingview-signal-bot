"""
TradingView Signal Bot -> Telegram
------------------------------------
Ei script ta ekta webhook server chalay. TradingView theke alert asle
eta receive kore ebong Telegram e message pathiye dey.

Setup:
1. .env file e BOT_TOKEN ar CHAT_ID diye dao (niche instruction ache)
2. `pip install -r requirements.txt`
3. `python app.py`
4. TradingView Alert er webhook URL e boshao: https://your-domain.com/webhook
"""

import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---- CONFIG (environment variable theke ashbe, .env file e set koro) ----
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")
# Optional: webhook e ekta secret token diye protect korte paro
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram_message(text: str):
    """Telegram e message pathay"""
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
    return response.ok, response.text


def format_signal_message(data: dict) -> str:
    """
    TradingView theke asha JSON data ke shundor kore format kore.
    TradingView Alert Message box e emon JSON pathate hobe:

    {
        "ticker": "{{ticker}}",
        "signal": "BUY",
        "price": "{{close}}",
        "time": "{{time}}",
        "timeframe": "{{interval}}"
    }
    """
    ticker = data.get("ticker", "N/A")
    signal = str(data.get("signal", "N/A")).upper()
    price = data.get("price", "N/A")
    timeframe = data.get("timeframe", "N/A")
    time_str = data.get("time", "N/A")

    emoji = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "ℹ️"

    message = (
        f"{emoji} <b>{signal} SIGNAL</b>\n\n"
        f"📊 <b>Pair/Ticker:</b> {ticker}\n"
        f"⏱ <b>Timeframe:</b> {timeframe}\n"
        f"💰 <b>Price:</b> {price}\n"
        f"🕒 <b>Time:</b> {time_str}"
    )
    return message


@app.route("/webhook", methods=["POST"])
def webhook():
    # ---- Optional secret check (URL e ?secret=xxx pathate hobe TradingView theke) ----
    if WEBHOOK_SECRET:
        received_secret = request.args.get("secret", "")
        if received_secret != WEBHOOK_SECRET:
            return jsonify({"status": "error", "message": "Invalid secret"}), 403

    # TradingView theke asha data (JSON ba plain text dujoi handle kora hocche)
    if request.is_json:
        data = request.get_json()
    else:
        # jodi plain text pathay, tahole raw text ke signal hisebe dhorbe
        raw_text = request.data.decode("utf-8")
        data = {"signal": raw_text}

    message = format_signal_message(data)
    ok, resp_text = send_telegram_message(message)

    if ok:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "detail": resp_text}), 500


@app.route("/", methods=["GET"])
def home():
    return "TradingView -> Telegram Signal Bot is running ✅"


@app.route("/test", methods=["GET"])
def test():
    """Browser e giye /test hit korle test message ashbe Telegram e"""
    ok, resp_text = send_telegram_message("✅ Test message: Bot thik moto kaj korche!")
    return jsonify({"sent": ok, "detail": resp_text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
