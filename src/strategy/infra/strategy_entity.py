from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.infra.base_entity import BaseEntity, EnumType
from src.infrastructure.timezone import TimeZone
from src.strategy.strategy_type import StrategyType


class StrategyEntity(BaseEntity):
    __tablename__ = "strategy"
    __table_args__ = {"extend_existing": True}

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tz: Mapped[TimeZone] = mapped_column(EnumType(TimeZone, length=7), nullable=False)
    target_volatility: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[StrategyType] = mapped_column(EnumType(StrategyType, length=5), nullable=False)
    last_executed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    tickers: Mapped[list[str]] = mapped_column(JSON, nullable=True)
