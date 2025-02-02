from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String
from src.common.adapter.out.persistence.base_entity import BaseEntity, EnumType
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any, Dict

from src.strategy.domain.strategy_type import StrategyType


class StrategyEntity(BaseEntity):
    __tablename__ = "strategy"
    name: Mapped[str] = mapped_column(String(30), index=True)
    invest_rate: Mapped[float] = mapped_column(Float)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    strategy_type: Mapped[StrategyType] = mapped_column(EnumType(StrategyType))
    last_run: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    additional_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True)
