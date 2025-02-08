from datetime import datetime
from typing import List

import pytz
from src.account.domain.account import Account
from strategy_new.strategy import Strategy, Symbol


class AMPMStrategy(Strategy):
    def __init__(
        self,
        name: str,
        account: Account,
        allocation: float,  # 전략 할당 비중 (0~1)
        symbols: List[Symbol],
        target_volatility: float = 0.01,
        timezone: str = "Etc/GMT+11",
    ):
        super().__init__(name, account, allocation, symbols)
        self.target_volatility = target_volatility
        self.timezone = pytz.timezone(timezone)

    def should_trade(self) -> bool:
        # 첫 실행 or 오늘 실행하지 않은 경우 or 오후에 실행하지 않은 경우
        return self.last_update is None or self.last_update.date() != datetime.now(self.timezone).date() or self.last_update.hour < 12

    def buy(self, symbol: Symbol):
        """매수"""
        pass

    def sell(self, symbol: Symbol):
        """매도"""
        pass

    def should_buy(self, symbol: Symbol) -> bool:
        """매수 조건 확인"""
        pass

    def should_sell(self, symbol: Symbol) -> bool:
        """매도 조건 확인"""
        pass

    def calculate_buy_weight(self, symbol: Symbol) -> float:
        """매수 비중 계산"""
        pass

    def calculate_sell_weight(self, symbol: Symbol) -> float:
        """매도 비중 계산"""
        pass
