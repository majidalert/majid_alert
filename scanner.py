import aiohttp
import asyncio
import time

from config import *
from utils import make_message
from state import AlertState
from market_history import MarketHistory


class MarketScanner:

    def __init__(self):

        self.state = AlertState(ALERT_COOLDOWN)
        self.history = MarketHistory()
        self.session = None

        # جلوگیری از هشدار تکراری
        self.last_alerts = {}


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

            return [
                x["symbol"]
                for x in data.get("result", {}).get("list", [])
                if x.get("quoteCoin") == "USDT"
            ]


    async def get_ticker(self, symbol):

        session = await self.get_session()

        async with session.get(
            BASE_URL +
            f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            return result[0] if result else None


    async def calculate_score(
        self,
        symbol,
        price,
        volume,
        change
    ):

        score = 0

        high3, low3 = await self.history.get_three_day_levels(symbol)

        high7, low7 = await self.history.get_week_levels(symbol)

        avg_volume = await self.history.get_average_volume(symbol)


        if low3:

            if ((price-low3)/low3)*100 >= MIN_RISE_FROM_LOW:
                score += 25


        if low7:

            if ((price-low7)/low7)*100 >= MIN_RISE_FROM_LOW:
                score += 25


        if high3:

            if ((high3-price)/high3)*100 <= THREE_DAY_RESISTANCE_DISTANCE:
                score += 20


        if high7:

            if ((high7-price)/high7)*100 <= WEEKLY_RESISTANCE_DISTANCE:
                score += 20


        if avg_volume and volume >= avg_volume * VOLUME_MULTIPLIER:
            score += 10


        return score, avg_volume



    async def scan(self):

        alerts = []

        symbols = await self.get_symbols()


        for symbol in symbols:

            try:

                ticker = await self.get_ticker(symbol)

                if not ticker:
                    continue


                price = float(ticker["lastPrice"])
                low = float(ticker["lowPrice24h"])
                volume = float(ticker["turnover24h"])


                if low <= 0:
                    continue


                change = ((price-low)/low)*100


                if change < MIN_RISE_FROM_LOW:
                    continue


                score, avg_volume = await self.calculate_score(
                    symbol,
                    price,
                    volume,
                    change
                )


                if score < MIN_SCORE:
                    continue


                message = make_message(
                    "🚀 پامپ",
                    symbol,
                    price,
                    change,
                    volume,
                    score
                )


                now = time.time()


                if symbol in self.last_alerts:

                    if now - self.last_alerts[symbol] < ALERT_COOLDOWN:
                        continue


                self.last_alerts[symbol] = now


                message += (
                    "\n🔥 قدرت هشدار: "
                    + ("⭐⭐⭐⭐⭐" if score >= 90 else "⭐⭐⭐")
                )


                alerts.append(message)


            except Exception as e:

                print(symbol, e)


            await asyncio.sleep(0.05)


        return alerts



    async def close(self):

        try:

            if self.session:
                await self.session.close()

        except Exception:
            pass


        try:

            await self.history.close()

        except Exception:
            pass