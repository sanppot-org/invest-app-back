from datetime import datetime
from typing import override

import pytz

from src.infrastructure.time_holder import TimeHolder
from src.infrastructure.timezone import TimeZone


class RealTimeHolder(TimeHolder):
    @override
    def get_now(self, timezone: TimeZone = TimeZone.UTC_P9) -> datetime:
        return datetime.now(pytz.timezone(timezone))

    @override
    def is_morning(self, timezone: TimeZone = TimeZone.UTC_P9) -> bool:
        return self.get_now(timezone).hour < 12

    @override
    def is_afternoon(self, timezone: TimeZone = TimeZone.UTC_P9) -> bool:
        return not self.is_morning