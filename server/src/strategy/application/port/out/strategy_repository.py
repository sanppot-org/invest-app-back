from abc import abstractmethod
from typing import List
from src.common.application.port.out.repository import Repository
from src.strategy.domain.strategy import Strategy


class StrategyRepository(Repository[Strategy]):
    @abstractmethod
    def find_all_active(self) -> List[Strategy]:
        pass
