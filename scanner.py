import aiohttp
import asyncio

from config import *
from utils import make_message
from state import AlertState
from market_history import MarketHistory


class MarketScanner:

    def __init__(self):

        self.state = AlertState(ALERT_COOLDOWN)
        self.history = MarketHistory()
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
            BASE_URL +
            f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            if not result:
                return None

            return result[0]


    async def calculate_score(self, symbol, price):

        score = 0

        high3, low3 = await self.history.get_three_day_levels(symbol)
        high7, low7 = await self.history.get_week_levels(symbol)
        avg_volume = await self.history.get_average_volume(symbol)


        if low3:

            rise3 = ((price - low3) / low3) * 100

            if rise3 >= MIN_RISE_FROM_LOW:
                score += 25


        if low7:

            rise7 = ((price - low7) / low7) * 100

            if rise7 >= MIN_RISE_FROM_LOW:
                score += 25


        if high3:

            distance = ((high3 - price) / high3) * 100

            if distance <= THREE_DAY_RESISTANCE_DISTANCE:
                score += 20


        if high7:

            distance = ((high7 - price) / high7) * 100

            if distance <= WEEKLY_RESISTANCE_DISTANCE:
                score += 20


        return score, high3, high7, avg_volume



    async def scan(self):

        alerts = []

        symbols = await self.get_symbols()

        checked = 0


        for symbol in symbols:

            try:

                checked += 1

                ticker = await self.get_ticker(symbol)

                if not ticker:
                    continue


                last = ticker.get("lastPrice")
                high = ticker.get("highPrice24h")
                low = ticker.get("lowPrice24h")
                volume = ticker.get("turnover24h")


                if None in (last, high, low, volume):
                    continue


                price = float(last)
                high24 = float(high)
                low24 = float(low)
                volume = float(volume)


                if low24 <= 0:
                    continue


                change = ((price-low24)/low24)*100
                drop = ((high24-price)/high24)*100


                score, high3, high7, avg_volume = await self.calculate_score(
                    symbol,
                    price
                )


                if change >= 20:
                    score += 10

                if change >= 50:
                    score += 15


                if drop >= 20:
                    score += 10


                if avg_volume > 0 and volume >= avg_volume * 3:
                    score += 15


                pump_scalp = (
                    change >= 20 and
                    avg_volume > 0 and
                    volume >= avg_volume * 2
                )


                dump_signal = (
                    drop >= 20 and
                    avg_volume > 0 and
                    volume >= avg_volume * 2
                )


                daily_distance = (
                    (high24-price)/high24
                )*100


                short_signal = (
                    change >= 80 and
                    daily_distance <= DAILY_RESISTANCE_DISTANCE and
                    avg_volume > 0 and
                    volume >= avg_volume * 3
                )


                score = min(score,100)


                if score < MIN_SCORE:
                    continue



                if short_signal and pump_scalp:

                    title = "⚠️ پامپ هیجانی + بررسی SHORT"

                elif short_signal:

                    title = "🟥 بررسی SHORT"

                elif pump_scalp:

                    title = "🚀 پامپ هیجانی"

                elif dump_signal:

                    title = "📉 دامپ هیجانی"

                else:

                    title = "📊 حرکت غیرعادی"



                if not self.state.can_send(symbol,title):
                    continue


                message = make_message(
                    title,
                    symbol,
                    price,
                    change,
                    volume,
                    score
                )


                if short_signal:

                    message += (
                        f"\n\n📉 SHORT PLAN"
                        f"\n🎯 ورود: {price:.8f}"
                        f"\n🛑 حد ضرر: {high24*1.02:.8f}"
                        f"\n🎯 TP1: {price*0.95:.8f}"
                        f"\n🎯 TP2: {price*0.90:.8f}"
                        f"\n🎯 TP3: {price*0.85:.8f}"
                    )


                alerts.append(message)


            except Exception as e:

                print("ERROR:", symbol, e)


            await asyncio.sleep(0.05)


        print(
            "Coins Checked:",
            checked,
            "Alerts:",
            len(alerts)
        )


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