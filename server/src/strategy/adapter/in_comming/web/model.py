from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from src.common.domain.type import Market, TimeUnit
from src.strategy.domain.strategy_entity import StrategyEntity
from src.strategy.domain.interval import Interval
from src.strategy.domain.stock_info import StockInfo


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


class StrategyUpsertReq(BaseModel):
    name: str
    invest_rate: float = Field(..., ge=0, le=1)
    stocks: Dict[str, StockInfoReq]
    interval: IntervalReq
    market: Market
    account_id: int
    is_active: Optional[bool] = False

    def to_entity(self) -> StrategyEntity:
        return StrategyEntity(
            id=None,
            name=self.name,
            invest_rate=self.invest_rate,
            stocks={k: v.toDomain() for k, v in self.stocks.items()},
            interval=self.interval.toDomain(),
            account_id=self.account_id,
            market=self.market,
            is_active=self.is_active or False,
            last_run=None,
        )
