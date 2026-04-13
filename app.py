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
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            response = requests.get(url)
            data = response.json()

            current_price = float(data["price"])

            if last_price is None:
                signal = "WAIT"
            elif current_price > last_price:
                signal = "HIGHER"
            else:
                signal = "LOWER"

            latest_signals = [
                {
                    "symbol": "BTC/USDT",
                    "signal": signal,
                    "price": current_price
                }
            ]

            last_price = current_price

            print("Updated:", latest_signals)

        except Exception as e:
            print("Error:", e)

        time.sleep(10)

@app.route("/signals")
def signals():
    return jsonify(latest_signals)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
