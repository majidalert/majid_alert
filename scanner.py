import requests

class MarketScanner:

    BINANCE_URL = "https://fapi.binance.com/fapi/v1/ticker/24hr"

    async def scan(self):

        alerts = []

        try:

            data = requests.get(self.BINANCE_URL, timeout=10).json()

            for coin in data:

                symbol = coin["symbol"]

                if not symbol.endswith("USDT"):
                    continue

                change = float(coin["priceChangePercent"])

                if change >= 10:

                    alerts.append(
                        f"🚀 PUMP\n\n"
                        f"📈 {symbol}\n"
                        f"رشد 24 ساعته: {change:.2f}%"
                    )

                elif change <= -10:

                    alerts.append(
                        f"📉 DUMP\n\n"
                        f"📉 {symbol}\n"
                        f"ریزش 24 ساعته: {change:.2f}%"
                    )

        except Exception as e:
            print(e)

        return alerts