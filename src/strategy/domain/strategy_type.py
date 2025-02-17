from enum import Enum


class StrategyType(Enum):
    STATIC_ASSET = "STATIC_ASSET"
    COIN = "COIN"
    VOLATILITY_BREAKOUT = "VOLATILITY_BREAKOUT"
    AM_PM = "AM_PM"
