from enum import Enum


class StrategyType(Enum):
    AMPM = "오전오후"
    VOL = "변동성돌파"

    def is_ampm(self):
        return self == StrategyType.AMPM