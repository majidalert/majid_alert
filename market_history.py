import aiohttp
from config import BASE_URL


class MarketHistory:

    def __init__(self):
        self.session = None

    async def get_session(self):

        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session

    async def get_klines(self, symbol, interval="60", limit=200):

        session = await self.get_session()

        url = (
            BASE_URL
            + "/v5/market/kline"
            + f"?category=linear"
            + f"&symbol={symbol}"
            + f"&interval={interval}"
            + f"&limit={limit}"
        )

        async with session.get(url) as response:

            data = await response.json(content_type=None)

            return data.get("result", {}).get("list", [])

    async def get_three_day_levels(self, symbol):

        candles = await self.get_klines(symbol, "60", 72)

        if not candles:
            return None, None

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return max(highs), min(lows)

    async def get_week_levels(self, symbol):

        candles = await self.get_klines(symbol, "60", 168)

        if not candles:
            return None, None

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return max(highs), min(lows)

    async def get_average_volume(self, symbol):

        candles = await self.get_klines(symbol, "60", 24)

        if not candles:
            return 0

        volumes = [float(c[5]) for c in candles]

        return sum(volumes) / len(volumes)

    async def close(self):

        if self.session:

            await self.session.close()