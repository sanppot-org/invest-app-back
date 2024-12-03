from typing import List, Optional
from pydantic import BaseModel
from domain.type import TimeUnit
from infra.persistance.model import Interval
from infra.persistance.schema import Account, Strategy
from domain.stock_info import StockInfo


class StockInfoReq(BaseModel):
    code: str
    target_rate: Optional[float] = None
    rebalance_amt: Optional[int] = None

    def toDomain(self) -> StockInfo:
        return StockInfo(
            code=self.code,
            target_rate=self.target_rate,
            rebalance_amt=self.rebalance_amt,
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
    env: Optional[str] = None
    stocks: list[StockInfoReq]
    interval: Optional[IntervalReq] = None

    def toDomain(self) -> Strategy:
        return Strategy(
            name=self.name,
            invest_rate=self.invest_rate,
            env=self.env,
            stocks=[stock.toDomain() for stock in self.stocks],
            interval=self.interval.toDomain(),
        )


class AccountCreateReq(BaseModel):
    name: str
    number: str
    product_code: str
    app_key: str
    secret_key: str
    url_base: str
    token: Optional[str] = None

    def toDomain(self) -> Account:
        return Account(
            name=self.name,
            number=self.number,
            product_code=self.product_code,
            app_key=self.app_key,
            secret_key=self.secret_key,
            url_base=self.url_base,
            token=self.token,
        )
