import time


class AlertState:
    """
    جلوگیری از ارسال هشدار تکراری
    """

    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.cache = {}

    def can_send(self, symbol: str, alert_type: str) -> bool:

        key = f"{symbol}_{alert_type}"

        now = time.time()

        if key not in self.cache:
            self.cache[key] = now
            return True

        if now - self.cache[key] >= self.cooldown:
            self.cache[key] = now
            return True

        return False

    def reset(self):
        self.cache.clear()

    def last_alert(self, symbol: str, alert_type: str):

        key = f"{symbol}_{alert_type}"

        return self.cache.get(key)