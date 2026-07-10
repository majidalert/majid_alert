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

    # -------------------------
    # 4 Hour
    # -------------------------

    async def get_four_hour_levels(self, symbol):

        candles = await self.get_klines(symbol, "240", 120)

        if not candles:
            return None, None

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return max(highs), min(lows)

    # -------------------------
    # 1 Day
    # -------------------------

    async def get_day_levels(self, symbol):

        candles = await self.get_klines(symbol, "D", 60)

        if not candles:
            return None, None

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return max(highs), min(lows)

    # -------------------------
    # 3 Day
    # -------------------------

    async def get_three_day_levels(self, symbol):

        candles = await self.get_klines(symbol, "60", 72)

        if not candles:
            return None, None

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return max(highs), min(lows)

    # -------------------------
    # Week
    # -------------------------

    async def get_week_levels(self, symbol):

        candles = await self.get_klines(symbol, "60", 168)

        if not candles:
            return None, None

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return max(highs), min(lows)

    # -------------------------
    # Average Volume
    # -------------------------

    async def get_average_volume(self, symbol):

        candles = await self.get_klines(symbol, "60", 24)

        if not candles:
            return 0

        volumes = [float(c[5]) for c in candles]

        return sum(volumes) / len(volumes)

    # -------------------------
    # Extension %
    # -------------------------

    async def get_extension_percent(self, symbol):

        high, low = await self.get_week_levels(symbol)

        if high is None or low is None:
            return None

        candles = await self.get_klines(symbol, "60", 1)

        if not candles:
            return None

        price = float(candles[0][4])

        if high == low:
            return 0

        return ((price - low) / (high - low)) * 100

    async def close(self):

        if self.session:

            await self.session.close()