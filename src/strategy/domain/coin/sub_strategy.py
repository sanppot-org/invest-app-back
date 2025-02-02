from abc import ABC, abstractmethod

from src.account.domain.account import Account
from src.common.adapter.out.upbit_df_holder import UpbitDfHolder
from src.common.domain.time_util import TimeUtil


class SubStrategy(ABC):
    """세부 전략의 추상 클래스"""

    def __init__(self, time_util: TimeUtil, target_volatility: float = 0.1):
        self.time_util = time_util
        self.target_volatility = target_volatility

    @abstractmethod
    def trade(self, account: Account, ticker: str, amount: float, upbit_df_holder: UpbitDfHolder):
        """매수/매도"""
        pass
