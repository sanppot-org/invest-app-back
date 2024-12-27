from dataclasses import dataclass
from typing import Dict

from src.common.domain.type import Market
from src.strategy.domain.interval import Interval
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy import StrategyDomainModel


@dataclass
class StrategyCreateCommand:
    name: str
    invest_rate: float
    stocks: Dict[str, StockInfo]
    interval: Interval
    market: Market
    account_id: int
    is_active: bool

    @classmethod
    def of(cls, strategy: StrategyDomainModel) -> "StrategyCreateCommand":
        return cls(
            name=strategy.name,
            invest_rate=strategy.invest_rate,
            stocks=strategy.stocks,
            interval=strategy.interval,
            market=strategy.market,
            account_id=strategy.account_id,
            is_active=strategy.is_active,
        )
