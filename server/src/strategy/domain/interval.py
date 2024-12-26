from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import TimeUnit


@dataclass
class Interval:
    time_unit: TimeUnit
    values: List[int]

    def to_dict(self):
        return {
            "time_unit": self.time_unit.value,
            "values": self.values,
        }

    def is_month(self):
        return self.time_unit == TimeUnit.MONTH

    def check_is_time_to_rebalance(self, now: datetime, last_run: datetime | None):
        if self.time_unit.is_month():
            this_month = now.month

            if this_month not in self.values or (last_run is not None and this_month == last_run.month):
                raise InvestAppException(exception_type=ExeptionType.NOT_TIME_TO_REBALANCE)
