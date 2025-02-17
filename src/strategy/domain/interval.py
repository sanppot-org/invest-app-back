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

    def is_time_to_rebalance(self, now: datetime, last_run: datetime) -> bool:
        if self.time_unit.is_month():
            this_month = now.month

            return this_month in self.values and this_month != last_run.month

        raise InvestAppException(
            ExeptionType.NOT_TIME_TO_REBALANCE,
            f"time_unit={self.time_unit}, values={self.values}, last_run={last_run}",
        )
