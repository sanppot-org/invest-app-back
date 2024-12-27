from abc import ABC, abstractmethod
from typing import List
from src.common.application.port.out.repository import Repository
from src.strategy.domain.strategy import StrategyDomainModel
from src.strategy.domain.strategy_upsert_command import StrategyCreateCommand


class StrategyRepository(Repository[StrategyCreateCommand, StrategyDomainModel], ABC):
    @abstractmethod
    def find_all_active(self) -> List[StrategyDomainModel]:
        pass
