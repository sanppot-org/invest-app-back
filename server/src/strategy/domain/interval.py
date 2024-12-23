from dataclasses import dataclass
from typing import List

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
