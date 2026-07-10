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
            BASE_URL +
            f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            if not result:
                return None

            return result[0]


    async def get_candles(self, symbol, interval, limit=100):

        session = await self.get_session()

        url = (
            BASE_URL +
            f"/v5/market/kline?"
            f"category=linear&symbol={symbol}"
            f"&interval={interval}&limit={limit}"
        )

        async with session.get(url) as response:

            data = await response.json(content_type=None)

            return (
                data.get("result", {})
                .get("list", [])
            )


    async def get_high(self, symbol, interval):

        candles = await self.get_candles(
            symbol,
            interval
        )

        if not candles:
            return None

        return max(
            float(c[2])
            for c in candles
        )


    async def get_average_volume(self, symbol):

        candles = await self.get_candles(
            symbol,
            "15",
            50
        )

        if not candles:
            return 0

        volumes = [
            float(c[6])
            for c in candles
        ]

        return sum(volumes) / len(volumes)


    async def volume_check(self, symbol, volume):

        avg = await self.get_average_volume(
            symbol
        )

        if avg <= 0:
            return False

        return volume >= avg * 2
            async def breakout_check(self, symbol, price):

        levels = [
            ("4H", "240"),
            ("1D", "D"),
            ("1W", "W")
        ]

        breakout = {}

        for name, interval in levels:

            high = await self.get_high(
                symbol,
                interval
            )

            if high:

                if price > high:

                    breakout[name] = high


        return breakout



    async def pullback_check(self, symbol, price):

        candles = await self.get_candles(
            symbol,
            "15",
            50
        )

        if not candles:
            return False


        recent_high = max(
            float(c[2])
            for c in candles
        )


        distance = (
            (recent_high - price)
            /
            recent_high
        ) * 100


        if 0 <= distance <= 1.5:

            return True


        return False



    async def pump_check(self, price, low):

        if low <= 0:
            return False


        move = (
            (price - low)
            /
            low
        ) * 100


        return move >= PUMP_PERCENT



    async def dump_check(self, price, high):

        if high <= 0:
            return False


        drop = (
            (high - price)
            /
            high
        ) * 100


        return drop >= DUMP_PERCENT



    async def resistance_check(self, symbol, price):

        resistance = {}

        levels = [
            (
                "4H",
                "240",
                FOUR_HOUR_RESISTANCE_DISTANCE
            ),
            (
                "1D",
                "D",
                DAILY_RESISTANCE_DISTANCE
            ),
            (
                "1W",
                "W",
                WEEKLY_RESISTANCE_DISTANCE
            )
        ]


        for name, interval, limit in levels:

            try:

                high = await self.get_high(
                    symbol,
                    interval
                )


                if high:

                    distance = (
                        (high - price)
                        /
                        high
                    ) * 100


                    if 0 <= distance <= limit:

                        resistance[name] = high


            except Exception as e:

                print(
                    "Resistance Error:",
                    symbol,
                    e
                )


        return resistance
            async def scan(self):

        alerts = []

        symbols = await self.get_symbols()


        for symbol in symbols:

            try:

                ticker = await self.get_ticker(symbol)

                if ticker is None:
                    continue


                last_price = float(
                    ticker.get("lastPrice")
                )

                high_price = float(
                    ticker.get("highPrice24h")
                )

                low_price = float(
                    ticker.get("lowPrice24h")
                )

                volume = float(
                    ticker.get("turnover24h")
                )


                if low_price <= 0:
                    continue


                change = (
                    (last_price - low_price)
                    /
                    low_price
                ) * 100


                score = 0


                pump = await self.pump_check(
                    last_price,
                    low_price
                )


                dump = await self.dump_check(
                    last_price,
                    high_price
                )


                volume_spike = await self.volume_check(
                    symbol,
                    volume
                )


                breakout = await self.breakout_check(
                    symbol,
                    last_price
                )


                pullback = await self.pullback_check(
                    symbol,
                    last_price
                )


                resistance = await self.resistance_check(
                    symbol,
                    last_price
                )


                if pump:
                    score += 25


                if dump:
                    score += 25


                if volume_spike:
                    score += 20


                if breakout:
                    score += 30


                if pullback:
                    score += 15


                if resistance:
                    score += 20



                if (
                    score >= MIN_SCORE
                    and
                    self.state.can_send(
                        symbol,
                        "ALERT"
                    )
                ):


                    title = "🚨 هشدار بازار"


                    if breakout and volume_spike:

                        title = (
                            "🚀 Breakout + Volume غیرعادی"
                        )

                    elif pump and volume_spike:

                        title = (
                            "🔥 پامپ هیجانی + حجم بالا"
                        )

                    elif dump:

                        title = (
                            "🟥 دامپ شدید"
                        )

                    elif pullback:

                        title = (
                            "🔄 Pullback بعد از حرکت"
                        )

                    elif resistance:

                        title = (
                            "⚠️ نزدیک مقاومت مهم"
                        )


                    alerts.append(
                        make_message(
                            title,
                            symbol,
                            last_price,
                            change,
                            volume,
                            score,
                            resistance=resistance
                        )
                    )


            except Exception as e:

                print(
                    symbol,
                    e
                )


            await asyncio.sleep(0.05)


        return alerts



    async def close(self):

        if self.session:

            await self.session.close()