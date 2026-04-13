from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import random
import requests
app = Flask(__name__)
CORS(app)

latest_signals = []

def run_bot():
    global latest_signals

    last_price = None

    while True:
        try:
            # 🔥 BTC prijs ophalen (Binance API)
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            response = requests.get(url)
            data = response.json()

            current_price = float(data["price"])

            # eerste run
            if last_price is None:
                signal = "NEUTRAL"
                score = 5
            else:
                if current_price > last_price:
                    signal = "HIGHER"
                    score = 7
                else:
                    signal = "LOWER"
                    score = 7

            last_price = current_price

            latest_signals = [
                {
                    "symbol": "BTC/USDT",
                    "signal": signal,
                    "score": score,
                    "price": current_price
                }
            ]

            print("Updated signals:", latest_signals)

        except Exception as e:
            print("Error:", e)

        time.sleep(10)
       



@app.route("/signals")
def signals():
    return jsonify(latest_signals)

import os

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
