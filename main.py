import asyncio
import time

from scanner import MarketScanner
from telegram_bot import TelegramNotifier
from config import *


scanner = MarketScanner()
telegram = TelegramNotifier(BOT_TOKEN, CHAT_ID)


# جلوگیری از ارسال دوباره همان هشدار
sent_alerts = {}


async def run():

    print("=" * 50)
    print("🚨 MAJID ALERT AI PRO STARTED")
    print("=" * 50)


    while True:

        try:

            alerts = await scanner.scan()


            if alerts:

                print(f"{len(alerts)} Alert(s) Found")


                for alert in alerts:

                    try:

                        # تشخیص تکراری بر اساس نام ارز
                        lines = alert.split("\n")

                        key = lines[0].strip() if lines else alert.strip()


                        now = time.time()


                        if key in sent_alerts:

                            if now - sent_alerts[key] < ALERT_COOLDOWN:

                                print("Duplicate skipped:", key)

                                continue


                        sent_alerts[key] = now


                        await telegram.send(alert)


                    except Exception as e:

                        print("Telegram Error:", e)


            else:

                print("No Alert")


        except Exception as e:

            print("Scanner Error:", e)


        await asyncio.sleep(SCAN_INTERVAL)



async def shutdown():

    await scanner.close()



if __name__ == "__main__":

    try:

        asyncio.run(run())


    except KeyboardInterrupt:

        print("Stopped By User")


    finally:

        try:

            asyncio.run(shutdown())

        except:

            pass