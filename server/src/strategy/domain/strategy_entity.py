from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, TypeDecorator
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import Market, TimeUnit
from src.strategy.domain.interval import Interval
from src.strategy.domain.stock_info import StockInfo
from src.common.adapter.out.persistence.base_entity import BaseEntity, EnumType
from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict


class StockInfoDict(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: Dict[str, StockInfo], dialect):
        if value is not None:
            return {k: {"target_rate": v.target_rate} for k, v in value.items()}
        return None

    def process_result_value(self, value: dict, dialect):
        if value is not None:
            return {k: StockInfo(**v) for k, v in value.items()}
        return None


class IntervalType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: Interval, dialect):
        if value is not None:
            return value.to_dict()
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return Interval(time_unit=TimeUnit(value["time_unit"]), values=value["values"])
        return None


class StrategyEntity(BaseEntity):
    __tablename__ = "strategy"
    name: Mapped[str] = mapped_column(String(30), index=True)
    invest_rate: Mapped[float] = mapped_column(Float)
    market: Mapped[Market] = mapped_column(EnumType(Market))
    stocks: Mapped[Dict[str, StockInfo]] = mapped_column(StockInfoDict, nullable=True)
    interval: Mapped[Interval] = mapped_column(IntervalType)
    last_run: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def validate_portfolio_rate(self):
        if sum([stock.target_rate for stock in self.stocks.values()]) != 1:
            raise InvestAppException(
                ExeptionType.INVALID_PORTFOLIO_RATE,
                {ticker: stock.target_rate for ticker, stock in self.stocks.items()},
            )

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate

    def get_stocks(self) -> Dict[str, StockInfo]:
        return self.stocks

    def complete_rebalance(self):
        self.last_run = datetime.now()

    def check_is_time_to_rebalance(self, now: datetime):
        self.interval.check_is_time_to_rebalance(now, self.last_run)

    def get_market(self) -> Market:
        return self.market

    def get_account_id(self) -> int:
        return self.account_id

    def update(self, entity: "StrategyEntity"):
        self.name = entity.name
        self.invest_rate = entity.invest_rate
        self.stocks = entity.stocks
        self.interval = entity.interval
        self.account_id = entity.account_id
        self.market = entity.market
        self.is_active = entity.is_active
