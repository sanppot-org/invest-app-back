from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, TypeDecorator
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
