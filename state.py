import time


class AlertState:
    """
    جلوگیری از ارسال هشدار تکراری
    """

    def __init__(self, cooldown):

        self.cooldown = cooldown
        self.cache = {}


    def can_send(
        self,
        symbol,
        alert_type,
        price=None
    ):

        key = f"{symbol}_{alert_type}"

        now = time.time()

        if key not in self.cache:

            self.cache[key] = {
                "time": now,
                "price": price
            }

            return True


        last = self.cache[key]

        elapsed = now - last["time"]


        # اگر زمان کول‌داون نگذشته باشد
        if elapsed < self.cooldown:

            if (
                price is not None
                and last["price"] is not None
            ):

                change = (
                    abs(
                        price - last["price"]
                    )
                    /
                    last["price"]
                ) * 100

                # اگر کمتر از ۱٪ تغییر کرده باشد
                # هشدار ارسال نشود
                if change < 1:
                    return False

            else:

                return False


        self.cache[key] = {

            "time": now,

            "price": price

        }

        return True


    def reset(self):

        self.cache.clear()


    def last_alert(
        self,
        symbol,
        alert_type
    ):

        key = f"{symbol}_{alert_type}"

        return self.cache.get(key)