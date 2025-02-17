from abc import abstractmethod
from typing import List
from src.common.application.port.out.repository import Repository
from src.strategy.domain.strategy_info import StrategyInfo


class StrategyRepository(Repository[StrategyInfo]):
    @abstractmethod
    def find_all_active(self) -> List[StrategyInfo]:
        pass
