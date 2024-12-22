from dataclasses import dataclass

from src.common.type import BrokerType


@dataclass
class Holding:
    ticker: str
    quantity: float
    avg_price: float
    current_price: float

    def calculate_value(self) -> float:
        return self.quantity * self.current_price


@dataclass
class Account:
    id: int
    broker_type: BrokerType
    balance: float
    holdings: dict[str, Holding]

    def calculate_total_value(self) -> float:
        return self.balance + sum(holding.calculate_value() for holding in self.holdings.values())
