import aiohttp

from config import *


class MarketHistory:

    def __init__(self):

        self.session = None


    async def get_session(self):

        if self.session is None:

            self.session = aiohttp.ClientSession()

        return self.session


    async def get_klines(

        self,

        symbol,

        interval="60",

        limit=200

    ):

        session = await self.get_session()

        url = (

            BASE_URL +

            "/v5/market/kline"

            f"?category=linear"

            f"&symbol={symbol}"

            f"&interval={interval}"

            f"&limit={limit}"

        )

        async with session.get(url) as response:

            data = await response.json(

                content_type=None

            )

            return (

                data.get("result", {})

                .get("list", [])

            )


    async def _levels(

        self,

        symbol,

        interval,

        limit

    ):

        candles = await self.get_klines(

            symbol,

            interval,

            limit

        )

        if not candles:

            return None, None

        highs = [

            float(c[2])

            for c in candles

        ]

        lows = [

            float(c[3])

            for c in candles

        ]

        return max(highs), min(lows)


    async def get_four_hour_levels(

        self,

        symbol

    ):

        return await self._levels(

            symbol,

            "240",

            60

        )


    async def get_day_levels(

        self,

        symbol

    ):

        return await self._levels(

            symbol,

            "D",

            30

        )


    async def get_three_day_levels(

        self,

        symbol

    ):

        return await self._levels(

            symbol,

            "60",

            72

        )


    async def get_week_levels(

        self,

        symbol

    ):

        return await self._levels(

            symbol,

            "60",

            168

        )


    async def get_average_volume(

        self,

        symbol

    ):

        candles = await self.get_klines(

            symbol,

            "60",

            24

        )

        if not candles:

            return 0

        volumes = [

            float(c[5])

            for c in candles

        ]

        return (

            sum(volumes)

            /

            len(volumes)

        )


    async def get_extension_percent(

        self,

        symbol,

        resistance

    ):

        _, low = await self.get_week_levels(

            symbol

        )

        if (

            low is None

            or resistance is None

            or resistance <= low

        ):

            return 0

        session = await self.get_session()

        ticker_url = (

            BASE_URL +

            f"/v5/market/tickers?category=linear&symbol={symbol}"

        )

        async with session.get(ticker_url) as response:

            data = await response.json(

                content_type=None

            )

            result = (

                data.get("result", {})

                .get("list", [])

            )

            if not result:

                return 0

            price = float(

                result[0]["lastPrice"]

            )

        return (

            (price - low)

            /

            (resistance - low)

        ) * 100


    async def close(self):

        if self.session:

            await self.session.close()