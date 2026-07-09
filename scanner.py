import aiohttp
import asyncio
from config import *
from utils import make_message
from state import AlertState


class MarketScanner:

    def __init__(self):
        self.state = AlertState(ALERT_COOLDOWN)
        self.session = None

    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def get_symbols(self):
        session = await self.get_session()

        async with session.get(
            BASE_URL + "/v5/market/instruments-info?category=linear"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            return [
                coin["symbol"]
                for coin in result
                if coin.get("quoteCoin") == "USDT"
            ]

    async def get_ticker(self, symbol):
        session = await self.get_session()

        async with session.get(
            BASE_URL + f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            if not result:
                return None

            return result[0]

    async def scan(self):

        alerts = []

        symbols = await self.get_symbols()

        for symbol in symbols:

            try:

                ticker = await self.get_ticker(symbol)

                if ticker is None:
                    continue

                vals = [
                    ticker.get("lastPrice"),
                    ticker.get("highPrice24h"),
                    ticker.get("lowPrice24h"),
                    ticker.get("turnover24h"),
                ]

                if any(v in (None, "") for v in vals):
                    continue

                last_price = float(vals[0])
                high_price = float(vals[1])
                low_price = float(vals[2])
                volume = float(vals[3])

                if low_price <= 0:
                    continue

                change = ((last_price - low_price) / low_price) * 100

                # فیلتر اصلی استراتژی مجید
                if change < MIN_RISE_FROM_LOW:
                    continue

                score = 0

                if change >= MIN_RISE_FROM_LOW:
                    score += 30

                if change >= PUMP_PERCENT:
                    score += 20

                distance_to_high = (
                    (high_price - last_price)
                    / high_price
                ) * 100

                if distance_to_high <= DAILY_RESISTANCE_DISTANCE:
                    score += 20

                if (
                    score >= MIN_SCORE
                    and self.state.can_send(symbol, "PUMP")
                ):

                    alerts.append(
                        make_message(
                            "🚀 پامپ",
                            symbol,
                            last_price,
                            change,
                            volume,
                            score,
                        )
                    )

            except Exception as e:
                print(symbol, e)

            await asyncio.sleep(0.05)

        return alerts

    async def close(self):

        if self.session:
            await self.session.close()