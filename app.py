def run_bot():
    global latest_signals

    print("BOT STARTED 🚀")

    last_price = None

    while True:
        try:
            print("Fetching price...")

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

            latest_signals = [{
                "symbol": "BTC/USDT",
                "signal": signal,
                "price": current_price
            }]

            last_price = current_price

            print("Updated:", latest_signals)

        except Exception as e:
            print("ERROR IN BOT:", e)

        time.sleep(10)
