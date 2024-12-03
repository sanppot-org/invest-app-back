from typing import List
from domain.type import TimeUnit


class StockInfo:
    def __init__(self, code: str, weight: float, count: int = 0):
        self.code = code
        self.weight = weight
        self.count = 0

    def __str__(self):
        return f"{self.code} {self.weight}"


class Interval:
    def __init__(self, time_unit: TimeUnit, value: List[int]):
        self.time_unit = time_unit
        self.value = value

    def __str__(self):
        return f"{self.start} {self.end}"

    def to_dict(self):
        return {
            "time_unit": self.time_unit.value,
            "value": self.value,
        }
