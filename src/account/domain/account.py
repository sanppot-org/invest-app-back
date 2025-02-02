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
        """
        잔고 조회
        """
        pass

    @abstractmethod
    def sell_all(self, ticker: str) -> None:
        """
        해당 종목 전체 매도
        """
        pass

    @abstractmethod
    def buy_market_order(self, ticker: Ticker, quantity: float | None = None, price: float | None = None):
        """
        시장가 매수

        :param ticker: 종목 티커
        :param quantity: 수량
        :param price: 가격
        """
        pass

    @abstractmethod
    def sell_market_order(self, ticker: Ticker, quantity: float) -> None:
        """
        시장가 매도

        :param ticker: 종목 티커
        :param quantity: 수량
        """
        pass

    @abstractmethod
    def get_holdings(self, market: Market = Market.KR) -> Dict[str, HoldingsInfo]:
        """
        보유 종목 조회
        """
        pass

    @abstractmethod
    def get_total_principal(self) -> float:
        """
        총 투자 금액 조회
        """
        pass

    @abstractmethod
    def get_revenue(self) -> float:
        """
        계좌의 총 수익률 조회
        """
        pass

    @abstractmethod
    def sell_all_holdings(self) -> None:
        """
        보유 종목 전체 매도
        """
        pass
