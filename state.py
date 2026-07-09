import time
import json
import os


CACHE_FILE = "alerts_cache.json"


class AlertState:
    """
    جلوگیری از ارسال هشدار تکراری
    با ذخیره دائمی
    """

    def __init__(self, cooldown):

        self.cooldown = cooldown
        self.cache = {}

        self.load()



    def _key(self, symbol, title):

        return (
            str(symbol).upper().strip()
            +
            "_"
            +
            str(title).strip()
        )



    def load(self):

        if os.path.exists(CACHE_FILE):

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

        key = self._key(
            symbol,
            title
        )

        now = time.time()



        if key not in self.cache:

            self.cache[key] = now

            self.save()

            return True



        last_time = self.cache[key]



        if now - last_time >= self.cooldown:

            self.cache[key] = now

            self.save()

            return True



        return False



    def update(self, symbol, title):

        key = self._key(
            symbol,
            title
        )

        self.cache[key] = time.time()

        self.save()



    def reset(self):

        self.cache.clear()

        self.save()



    def remove(self, symbol, title):

        key = self._key(
            symbol,
            title
        )


        if key in self.cache:

            del self.cache[key]

            self.save()



    def last_alert(self, symbol, title):

        key = self._key(
            symbol,
            title
        )

        return self.cache.get(key)



    def seconds_remaining(self, symbol, title):

        key = self._key(
            symbol,
            title
        )


        if key not in self.cache:

            return 0



        remain = (

            self.cooldown

            -

            (
                time.time()
                -
                self.cache[key]
            )

        )


        return max(
            0,
            int(remain)
        )