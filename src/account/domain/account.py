from abc import ABC, abstractmethod
from typing import Dict

from src.account.domain.account_info import AccountInfo
from src.account.domain.holdings import HoldingsInfo
from src.common.domain.ticker import Ticker
from src.common.domain.type import Market


class Account(ABC):
    def __init__(self, account_info: AccountInfo):
        self.account_info: AccountInfo = account_info

    @abstractmethod
    def get_balance(self, market: Market = Market.KR) -> float:
        pass

    @abstractmethod
    def buy_market_order(self, ticker: Ticker, quantity: int) -> None:
        pass

    @abstractmethod
    def sell_market_order(self, ticker: Ticker, quantity: int) -> None:
        pass

    @abstractmethod
    def get_holdings(self, market: Market = Market.KR) -> Dict[str, HoldingsInfo]:
        pass

    @abstractmethod
    def get_total_principal(self) -> float:
        pass

    @abstractmethod
    def get_revenue(self) -> float:
        """
        계좌의 총 수익률 조회
        """
        pass
