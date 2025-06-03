from abc import ABC, abstractmethod
from typing import Dict

from src.account.holdings import Holdings
from src.infrastructure.exchange.balance import Balance


class ExchangeClient(ABC):
    """
    거래소 클라이언트
    """

    @abstractmethod
    def get_balance(self) -> Balance:
        """
        잔고 조회
        """
        pass

    @abstractmethod
    def get_holdings(self) -> Dict[str, Holdings]:
        """
        보유 종목 조회
        """
        pass

    @abstractmethod
    def buy_limit_order(self, ticker: str, limit_price: float, volume: float):
        """
        지정가 매수
        limit_price: 지정가
        volume: 수량
        """
        pass

    @abstractmethod
    def buy_market_order(self, ticker: str, amount: float):
        """
        시장가 매수
        amount: 매수 금액
        """
        pass

    @abstractmethod
    def sell_limit_order(self, ticker: str, limit_price: float, volume: float):
        """
        지정가 매도
        limit_price: 지정가
        volume: 수량
        """
        pass

    @abstractmethod
    def sell_market_order(self, ticker: str, amount: float):
        """
        시장가 매도
        amount: 매수 금액
        """
        pass

    @abstractmethod
    def sell_all(self):
        """
        보유한 모든 종목 전량 시장가 매도
        """
        pass
