from typing import Dict, List, Optional
from pydantic import BaseModel

from src.domain.common.type import Market, TimeUnit
from src.domain.strategy.interval import Interval
from src.domain.strategy.stock_info import StockInfo
from src.domain.strategy.strategy import Strategy


class StockInfoReq(BaseModel):
    target_rate: Optional[float] = None
    rebalance_qty: Optional[int] = None

    def toDomain(self) -> StockInfo:
        return StockInfo(
            target_rate=self.target_rate,
            rebalance_qty=self.rebalance_qty,
        )


class IntervalReq(BaseModel):
    time_unit: TimeUnit
    value: List[int]

    def toDomain(self) -> Interval:
        return Interval(
            time_unit=self.time_unit,
            value=self.value,
        )


class StrategyCreateReq(BaseModel):
    name: str
    invest_rate: Optional[float] = None
    stocks: Dict[str, StockInfoReq]
    interval: Optional[IntervalReq] = None
    market: Market
    account_id: int

    def to_domain(self) -> Strategy:
        return Strategy(
            name=self.name,
            invest_rate=self.invest_rate,
            stocks={k: v.toDomain() for k, v in self.stocks.items()},
            interval=self.interval.toDomain(),
            account_id=self.account_id,
            market=self.market,
        )
