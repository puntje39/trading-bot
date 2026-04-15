from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import requests
import os

app = Flask(__name__)
CORS(app)

latest_signals = []

def run_bot():
    global latest_signals

    last_price = None

    while True:
        try:
            # BTC prijs ophalen
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            response = requests.get(url)
            data = response.json()

            current_price = float(data["price"])

            # eerste run
            if last_price is None:
                last_price = current_price
                continue

            # signaal bepalen
            if current_price > last_price:
                signal = "HIGHER"
                score = 7
            else:
                signal = "LOWER"
                score = 7

            latest_signals = [{
                "symbol": "BTC/USDT",
                "signal": signal,
                "score": score,
                "price": current_price
            }]

            print("Updated signals:", latest_signals)

            last_price = current_price

        except Exception as e:
            print("Error:", e)

        time.sleep(10)

# START BOT THREAD
threading.Thread(target=run_bot, daemon=True).start()

# API ENDPOINT
@app.route("/signals")
def get_signals():
    return jsonify(latest_signals)

# ROOT (handig voor testen)
@app.route("/")
def home():
    return "Trading bot is running 🚀"

# BELANGRIJK VOOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
