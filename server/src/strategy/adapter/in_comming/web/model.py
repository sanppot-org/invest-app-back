from typing import Dict, List
from pydantic import BaseModel, Field

from src.common.domain.type import Market, TimeUnit
from src.strategy.domain.interval import Interval
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy import Strategy


class StockInfoReq(BaseModel):
    target_rate: float = Field(..., ge=0, le=1)

    def toDomain(self) -> StockInfo:
        return StockInfo(target_rate=self.target_rate)


class IntervalReq(BaseModel):
    time_unit: TimeUnit
    values: List[int]

    def toDomain(self) -> Interval:
        return Interval(
            time_unit=self.time_unit,
            values=self.values,
        )


class StrategyCreateReq(BaseModel):
    name: str
    invest_rate: float = Field(..., ge=0, le=1)
    stocks: Dict[str, StockInfoReq]
    interval: IntervalReq
    market: Market
    account_id: int

    def to_domain(self) -> Strategy:
        return Strategy(
            id=None,
            name=self.name,
            invest_rate=self.invest_rate,
            stocks={k: v.toDomain() for k, v in self.stocks.items()},
            interval=self.interval.toDomain(),
            account_id=self.account_id,
            market=self.market,
            last_run=None,
        )
