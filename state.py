import time
import json
import os

CACHE_FILE = "alerts_cache.json"


class AlertState:

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

            print("Cache Save Error:", e)

    def can_send(
        self,
        symbol,
        title,
        score=None,
        multitrade_score=None
    ):

        key = self._key(symbol, title)

        now = time.time()

        if key not in self.cache:

            self.cache[key] = {
                "time": now,
                "count": 1,
                "score": score,
                "multitrade_score": multitrade_score
            }

            self.save()

            return True

        item = self.cache[key]

        last_time = item.get("time", 0)

        old_score = item.get("score", 0)

        old_multi = item.get(
            "multitrade_score",
            0
        )

        # اگر کیفیت هشدار بهتر شده باشد دوباره ارسال شود
        if (
            score is not None
            and score > old_score + 10
        ):

            self.update(
                symbol,
                title,
                score,
                multitrade_score
            )

            return True

        if (
            multitrade_score is not None
            and multitrade_score > old_multi + 10
        ):

            self.update(
                symbol,
                title,
                score,
                multitrade_score
            )

            return True

        if now - last_time >= self.cooldown:

            self.update(
                symbol,
                title,
                score,
                multitrade_score
            )

            return True

        return False

    def update(
        self,
        symbol,
        title,
        score=None,
        multitrade_score=None
    ):

        key = self._key(symbol, title)

        old = self.cache.get(key, {})

        count = 1

        if isinstance(old, dict):
            count = old.get("count", 0) + 1

        self.cache[key] = {
            "time": time.time(),
            "count": count,
            "score": score,
            "multitrade_score": multitrade_score
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

        return item.get("time")

    def alert_count(self, symbol, title):

        key = self._key(symbol, title)

        item = self.cache.get(key)

        if item is None:
            return 0

        return item.get("count", 0)

    def seconds_remaining(self, symbol, title):

        key = self._key(symbol, title)

        item = self.cache.get(key)

        if item is None:
            return 0

        remain = self.cooldown - (
            time.time() - item.get("time", 0)
        )

        return max(0, int(remain))