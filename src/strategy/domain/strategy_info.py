from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from src.strategy.domain.strategy_type import StrategyType


@dataclass
class StrategyInfo:
    id: Optional[int]
    name: str
    invest_rate: float
    account_id: int
    is_active: bool
    strategy_type: StrategyType
    last_run: Optional[datetime]
    additional_data: Optional[dict]

    def update(self, strategy: Self):
        self.name = strategy.name
        self.invest_rate = strategy.invest_rate
        self.account_id = strategy.account_id
        self.is_active = strategy.is_active
        self.last_run = strategy.last_run
        self.strategy_type = strategy.strategy_type
        self.additional_data = strategy.additional_data
