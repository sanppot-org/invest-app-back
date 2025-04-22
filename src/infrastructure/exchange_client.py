from abc import ABC, abstractmethod
from typing import Dict

from src.account.holdings import Holdings


class ExchangeClient(ABC):
    """
    거래소 클라이언트
    """

    @abstractmethod
    def get_balance(self) -> float:
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
