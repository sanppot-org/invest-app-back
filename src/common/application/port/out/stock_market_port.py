from abc import ABC, abstractmethod

from src.common.domain.type import Market
from src.common.domain.ticker import Ticker


class StockMarketQueryPort(ABC):
    @abstractmethod
    def is_market_open(self, market: Market):
        pass

    @abstractmethod
    def get_current_price(self, ticker: Ticker) -> float:
        pass
