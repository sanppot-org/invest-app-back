from abc import ABC, abstractmethod
from typing import List

from src.account.domain.account import Account
from src.common.domain.ticker import Ticker
from strategy_new.condition.strategy_condition import StrategyCondition


class Strategy(ABC):
    def __init__(
        self,
        name: str,
        account: Account,
        allocation: float,  # 전략 할당 비중 (0~1)
        tickers: List[Ticker],
        trade_condition: StrategyCondition,
        buy_condition: StrategyCondition,
        sell_condition: StrategyCondition,
    ):  # UTC-11
        self.name = name
        self.account = account
        self.allocation = allocation
        self.tickers = tickers
        self.trade_condition = trade_condition
        self.buy_condition = buy_condition
        self.sell_condition = sell_condition
        self.last_update = None

    def trade(self):
        if not self.should_trade():
            return

        for ticker in self.tickers:
            if self.should_buy(ticker):
                balance = self.account.get_balance()
                allocation_amount = balance * self.allocation
                buy_weight = self.calculate_buy_weight(ticker)
                investment_amount = allocation_amount * buy_weight
                if investment_amount > 0:
                    self.buy(ticker, investment_amount)

            if self.should_sell(ticker):
                balance = self.account.get_balance()
                allocation_amount = balance * self.allocation
                sell_weight = self.calculate_sell_weight(ticker)
                investment_amount = allocation_amount * sell_weight
                if investment_amount > 0:
                    self.sell(ticker, investment_amount)

    def should_trade(self) -> bool:
        return self.trade_condition.check_chain()

    def should_buy(self, ticker: Ticker) -> bool:
        return self.buy_condition.check_chain()

    def should_sell(self, ticker: Ticker) -> bool:
        return self.sell_condition.check_chain()

    @abstractmethod
    def buy(self, ticker: Ticker, allocation_amount: float):
        """매수"""
        pass

    @abstractmethod
    def sell(self, ticker: Ticker, allocation_amount: float):
        """매도"""
        pass

    @abstractmethod
    def calculate_buy_weight(self, ticker: Ticker) -> float:
        """매수 비중 계산"""
        pass

    @abstractmethod
    def calculate_sell_weight(self, ticker: Ticker) -> float:
        """매도 비중 계산"""
        pass
