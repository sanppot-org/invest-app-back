from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.account.domain.account import Account
from src.strategy.domain.strategy_type import StrategyType


@dataclass
class Strategy(ABC):
    id: Optional[int]
    name: str
    invest_rate: float
    account_id: int
    is_active: bool
    last_run: Optional[datetime]
    strategy_type: StrategyType

    @abstractmethod
    def trade(self, account: Account):
        pass

    def validate(self):
        pass

    def complete(self):
        self.last_run = datetime.now()

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate

    def get_account_id(self) -> int:
        return self.account_id

    def update(self, strategy: "Strategy"):
        self.name = strategy.name
        self.invest_rate = strategy.invest_rate
        self.account_id = strategy.account_id
        self.is_active = strategy.is_active
        self.last_run = strategy.last_run
        self.strategy_type = strategy.strategy_type
