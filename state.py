import time
import json
import os


CACHE_FILE = "alerts_cache.json"


class AlertState:

    """
    جلوگیری از ارسال هشدار تکراری
    هر نوع هشدار برای هر نماد به صورت مستقل ذخیره می‌شود.
    """

    def __init__(self, cooldown):

        self.cooldown = cooldown
        self.cache = {}

        self.load()


    def _key(self, symbol, title):

        return (
            str(symbol).upper().strip()
            + "_"
            + str(title).strip()
        )


    def load(self):

        if not os.path.exists(CACHE_FILE):
            self.cache = {}
            return

        try:

            with open(
                CACHE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.cache = json.load(f)

        except Exception:

            self.cache = {}


    def save(self):

        try:

            with open(
                CACHE_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.cache,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as e:

            print(
                "Cache Save Error:",
                e
            )


    def can_send(self, symbol, title):

        key = self._key(symbol, title)

        now = time.time()

        if key not in self.cache:

            self.cache[key] = {
                "time": now,
                "count": 1
            }

            self.save()

            return True


        item = self.cache[key]

        if isinstance(item, (int, float)):
            last_time = item
            count = 1
        else:
            last_time = item.get("time", 0)
            count = item.get("count", 1)

        if now - last_time >= self.cooldown:

            self.cache[key] = {
                "time": now,
                "count": count + 1
            }

            self.save()

            return True

        return False


    def update(self, symbol, title):

        key = self._key(symbol, title)

        old = self.cache.get(key, {})

        count = 1

        if isinstance(old, dict):
            count = old.get("count", 0) + 1

        self.cache[key] = {
            "time": time.time(),
            "count": count
        }

        self.save()


    def reset(self):

        self.cache = {}

        self.save()


    def remove(self, symbol, title):

        key = self._key(symbol, title)

        if key in self.cache:

            del self.cache[key]

            self.save()


    def last_alert(self, symbol, title):

        key = self._key(symbol, title)

        item = self.cache.get(key)

        if item is None:
            return None

        if isinstance(item, dict):
            return item.get("time")

        return item


    def alert_count(self, symbol, title):

        key = self._key(symbol, title)

        item = self.cache.get(key)

        if isinstance(item, dict):
            return item.get("count", 0)

        if item:
            return 1

        return 0


    def seconds_remaining(self, symbol, title):

        key = self._key(symbol, title)

        item = self.cache.get(key)

        if item is None:
            return 0

        if isinstance(item, dict):
            last_time = item.get("time", 0)
        else:
            last_time = item

        remain = self.cooldown - (time.time() - last_time)

        return max(0, int(remain))