import aiohttp
import asyncio
from config import *
from utils import make_message
from state import AlertState

class MarketScanner:
    def __init__(self):
        self.state=AlertState(ALERT_COOLDOWN)
        self.session=None
    async def get_session(self):
        if self.session is None:
            self.session=aiohttp.ClientSession()
        return self.session
    async def get_symbols(self):
        s=await self.get_session()
        async with s.get(BASE_URL+"/v5/market/instruments-info?category=linear") as r:
            data=await r.json(content_type=None)
            return [c["symbol"] for c in data.get("result",{}).get("list",[]) if c.get("quoteCoin")=="USDT"]
    async def get_ticker(self,symbol):
        s=await self.get_session()
        async with s.get(BASE_URL+f"/v5/market/tickers?category=linear&symbol={symbol}") as r:
            data=await r.json(content_type=None)
            lst=data.get("result",{}).get("list",[])
            return lst[0] if lst else None
    async def scan(self):
        alerts=[]
        for symbol in await self.get_symbols():
            try:
                t=await self.get_ticker(symbol)
                if not t: continue
                vals=[t.get("lastPrice"),t.get("highPrice24h"),t.get("lowPrice24h"),t.get("turnover24h")]
                if any(v in (None,"") for v in vals):
                    continue
                last=float(vals[0]); high=float(vals[1]); low=float(vals[2]); vol=float(vals[3])
                if low<=0: continue
                ch=((last-low)/low)*100
                score=40 if ch>=PUMP_PERCENT or ch<=DUMP_PERCENT else 0
                if ch>=PUMP_PERCENT and self.state.can_send(symbol,"PUMP"):
                    alerts.append(make_message("ð Ù¾Ø§ÙÙ¾",symbol,last,ch,vol,score))
                elif ch<=DUMP_PERCENT and self.state.can_send(symbol,"DUMP"):
                    alerts.append(make_message("ð Ø¯Ø§ÙÙ¾",symbol,last,ch,vol,score))
            except Exception as e:
                print(symbol,e)
            await asyncio.sleep(0.05)
        return alerts
    async def close(self):
        if self.session:
            await self.session.close()