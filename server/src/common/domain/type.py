from datetime import datetime
from enum import Enum

import pytz


class TriggerType(Enum):
    CRON = "cron"
    INTERVAL = "interval"
    DATE = "date"


class EnvType(Enum):
    REAL = "REAL"
    VIRTUAL = "VIRTUAL"


class Market(Enum):
    KR = "KR"
    US = "US"

    def is_kr(self):
        return self == Market.KR

    def is_us(self):
        return self == Market.US

    @property
    def tz(self):
        if self.is_kr():
            return pytz.timezone("Asia/Seoul")
        return pytz.timezone("America/New_York")

    def get_now(self) -> datetime:
        return datetime.now().astimezone(self.tz)

    def is_market_open_time(self):
        return self._is_market_open_time(self.get_now())

    def _is_market_open_time(self, now: datetime):
        if now.weekday() >= 5:
            return False

        if self.is_kr():
            # 한국 주식 시간 - 주말 제외, 9:00 ~ 15:25
            return now.hour >= 9 and (now.hour < 15 or (now.hour == 15 and now.minute <= 25))

        # 미국 주식 시간 (현지 시간) - 주말 제외, 10:00 ~ 16:00
        return now.hour >= 10 and now.hour <= 16


class TimeUnit(Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class BrokerType(Enum):
    KIS = "KIS"
    UPBIT = "UPBIT"

    def is_kis(self):
        return self == BrokerType.KIS
