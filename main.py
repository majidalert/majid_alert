import asyncio
import time

from scanner import MarketScanner
from telegram_bot import TelegramNotifier
from config import *


scanner = MarketScanner()
telegram = TelegramNotifier(BOT_TOKEN, CHAT_ID)


# ذخیره هشدارهای ارسال شده
sent_alerts = {}


def get_alert_key(alert):

    """
    استخراج کلید یکتا برای هر هشدار
    """

    for line in alert.split("\n"):

        line = line.strip()

        if "USDT" in line:

            return line


        if "ارز" in line:

            return line


    # اگر نام ارز پیدا نشد
    return alert[:80]



async def run():

    print("=" * 50)
    print("🚨 MAJID ALERT AI PRO STARTED")
    print("=" * 50)


    while True:

        try:

            alerts = await scanner.scan()


            if alerts:

                print(
                    f"{len(alerts)} Alert(s) Found"
                )


                for alert in alerts:


                    try:


                        key = get_alert_key(alert)


                        now = time.time()



                        if key in sent_alerts:


                            if (
                                now - sent_alerts[key]
                                < ALERT_COOLDOWN
                            ):

                                print(
                                    "Duplicate skipped:",
                                    key
                                )

                                continue



                        sent_alerts[key] = now



                        await telegram.send(alert)



                    except Exception as e:

                        print(
                            "Telegram Error:",
                            e
                        )



            else:

                print("No Alert")



        except Exception as e:

            print(
                "Scanner Error:",
                e
            )



        await asyncio.sleep(
            SCAN_INTERVAL
        )





async def shutdown():

    await scanner.close()





if __name__ == "__main__":


    try:


        asyncio.run(run())



    except KeyboardInterrupt:


        print(
            "Stopped By User"
        )



    finally:


        try:

            asyncio.run(
                shutdown()
            )


        except:


            pass