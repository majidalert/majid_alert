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


    async def get_high(self, symbol, interval):

        session = await self.get_session()

        url = (
            BASE_URL +
            f"/v5/market/kline?"
            f"category=linear&symbol={symbol}"
            f"&interval={interval}&limit=100"
        )

        async with session.get(url) as response:

            data = await response.json(content_type=None)

            candles = (
                data.get("result", {})
                .get("list", [])
            )

            if not candles:
                return None

            return max(
                float(candle[2])
                for candle in candles
            )


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


                if change >= MIN_RISE_FROM_LOW:
                    score += 30


                if change >= PUMP_PERCENT:
                    score += 20



                resistance = await self.resistance_check(
                    symbol,
                    last_price
                )


                if resistance:

                    score += 30



                distance = (
                    (high_price - last_price)
                    /
                    high_price
                ) * 100


                if distance <= DAILY_RESISTANCE_DISTANCE:

                    score += 20



                if (
                    score >= MIN_SCORE
                    and
                    self.state.can_send(
                        symbol,
                        "ALERT"
                    )
                ):


                    title = "🚀 پامپ قوی"


                    if resistance:

                        title = (
                            "⚠️ نزدیک مقاومت مهم "
                            "(4H / 1D / 1W)"
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