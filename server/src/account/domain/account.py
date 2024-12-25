from abc import ABC, abstractmethod

from src.account.domain.account_info import AccountInfo
from src.account.domain.holdings import HoldingsInfo
from src.common.domain.type import Market


class Account(ABC):
    def __init__(self, account_info: AccountInfo):
        self.account_info: AccountInfo = account_info

    @abstractmethod
    def get_balance(self, market: Market = Market.KR) -> float:
        pass

    @abstractmethod
    def buy_market_order(self, ticker: str, quantity: int) -> None:
        pass

    @abstractmethod
    def sell_market_order(self, ticker: str, quantity: int) -> None:
        pass

    @abstractmethod
    def get_holdings(self, market: Market = Market.KR) -> dict[str, HoldingsInfo]:
        pass
