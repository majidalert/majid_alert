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
        url = BASE_URL + "/v5/market/instruments-info?category=linear"
        async with session.get(url) as response:
            data = await response.json()
            result = data.get("result", {}).get("list", [])
            return [c["symbol"] for c in result if c.get("quoteCoin") == "USDT"]

    async def get_ticker(self, symbol):
        session = await self.get_session()
        url = BASE_URL + f"/v5/market/tickers?category=linear&symbol={symbol}"
        async with session.get(url) as response:
            data = await response.json()
            return data["result"]["list"][0]

    async def scan(self):
        alerts = []
        try:
            symbols = await self.get_symbols()
            for symbol in symbols:
                try:
                    ticker = await self.get_ticker(symbol)
                    last_price = float(ticker["lastPrice"])
                    high_price = float(ticker["highPrice24h"])
                    low_price = float(ticker["lowPrice24h"])
                    volume = float(ticker["turnover24h"])

                    if low_price == 0:
                        continue

                    change = ((last_price - low_price) / low_price) * 100
                    score = 0

                    if change >= PUMP_PERCENT:
                        score += 40
                    if change <= DUMP_PERCENT:
                        score += 40

                    distance = ((high_price - last_price) / high_price) * 100

                    if distance <= NEAR_HIGH_PERCENT and self.state.can_send(symbol, "HIGH"):
                        alerts.append(make_message("ð¥ ÙØ²Ø¯ÛÚ© Ø³ÙÙ Û²Û´ Ø³Ø§Ø¹ØªÙ", symbol, last_price, change, volume, score + 20))

                    if change >= PUMP_PERCENT and self.state.can_send(symbol, "PUMP"):
                        alerts.append(make_message("ð Ù¾Ø§ÙÙ¾", symbol, last_price, change, volume, score))

                    if change <= DUMP_PERCENT and self.state.can_send(symbol, "DUMP"):
                        alerts.append(make_message("ð Ø¯Ø§ÙÙ¾", symbol, last_price, change, volume, score))

                except Exception as e:
                    print(f"{symbol}: {e}")

                await asyncio.sleep(0.05)

        except Exception as e:
            print("Scanner:", e)

        return alerts

    async def close(self):
        if self.session:
            await self.session.close()
