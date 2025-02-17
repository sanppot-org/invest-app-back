from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from src.account.domain.account import Account
from src.common.domain.ticker import Ticker


class Strategy(ABC):
    def __init__(
        self,
        name: str,
        account: Account,
        allocation: float,  # 전략 할당 비중 (0~1)
        tickers: List[Ticker],
        last_run: Optional[datetime] = None,
    ):
        self.name = name
        self.account = account
        self.allocation = allocation
        self.tickers = tickers
        self.last_run = last_run

    def trade(self):
        if not self.should_trade():
            return

        for ticker in self.tickers:
            if self.should_buy(ticker):
                balance = self.account.get_balance()
                allocation_amount = balance * self.allocation
                buy_weight = self.get_buy_weight(ticker)
                investment_amount = allocation_amount * buy_weight
                if investment_amount > 0:
                    self.buy(ticker, investment_amount)

            if self.should_sell(ticker):
                balance = self.account.get_balance()
                allocation_amount = balance * self.allocation
                sell_weight = self.get_sell_weight(ticker)
                investment_amount = allocation_amount * sell_weight
                if investment_amount > 0:
                    self.sell(ticker, investment_amount)

    @abstractmethod
    def should_buy(self, ticker: Ticker) -> bool:
        """매수 조건 확인"""
        pass

    @abstractmethod
    def should_sell(self, ticker: Ticker) -> bool:
        """매도 조건 확인"""
        pass

    @abstractmethod
    def buy(self, ticker: Ticker, allocation_amount: float):
        """매수"""
        pass

    @abstractmethod
    def sell(self, ticker: Ticker, allocation_amount: float):
        """매도"""
        pass

    def should_trade(self) -> bool:
        """전략 실행 조건 확인"""
        return True

    def get_buy_weight(self, ticker: Ticker) -> float:
        """매수 비중 계산"""
        return 1

    def get_sell_weight(self, ticker: Ticker) -> float:
        """매도 비중 계산"""
        return 1
