import time


class AlertState:
    """
    جلوگیری از ارسال هشدار تکراری
    """

    def __init__(self, cooldown):

        self.cooldown = cooldown

        self.cache = {}

    def _key(self, symbol, alert_type):

        return f"{symbol}_{alert_type}"

    def can_send(self, symbol, alert_type):

        key = self._key(symbol, alert_type)

        now = time.time()

        if key not in self.cache:

            self.cache[key] = now

            return True

        last_time = self.cache[key]

        if now - last_time >= self.cooldown:

            self.cache[key] = now

            return True

        return False

    def update(self, symbol, alert_type):

        key = self._key(symbol, alert_type)

        self.cache[key] = time.time()

    def reset(self):

        self.cache.clear()

    def remove(self, symbol, alert_type):

        key = self._key(symbol, alert_type)

        if key in self.cache:

            del self.cache[key]

    def last_alert(self, symbol, alert_type):

        key = self._key(symbol, alert_type)

        return self.cache.get(key)

    def seconds_remaining(self, symbol, alert_type):

        key = self._key(symbol, alert_type)

        if key not in self.cache:

            return 0

        remain = self.cooldown - (time.time() - self.cache[key])

        return max(0, int(remain))