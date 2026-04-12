from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

latest_signals = []

def run_bot():
    global latest_signals

    while True:
        latest_signals = [
            {"symbol": "BTC/USDT", "signal": "HIGHER 📈", "score": 6}
        ]
        print("Updated signals")
        time.sleep(10)

threading.Thread(target=run_bot).start()

@app.route("/signals")
def signals():
    return jsonify(latest_signals)

import os

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
