from src.common.domain.type import Market


from abc import ABC, abstractmethod


class StockMarketQueryPort(ABC):
    @abstractmethod
    def is_market_open(self, market: Market):
        pass

    @abstractmethod
    def get_current_price(self, ticker: str) -> float:
        pass
