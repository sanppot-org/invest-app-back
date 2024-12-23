from src.common.domain.type import Market


from abc import ABC, abstractmethod


class StockMarketClient(ABC):
    @abstractmethod
    def is_market_open(self, market: Market) -> bool:
        pass
