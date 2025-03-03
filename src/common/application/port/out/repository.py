from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from src.common.domain.type import BrokerType

Model = TypeVar("Model")


class Repository(ABC, Generic[Model]):
    @abstractmethod
    def save(self, model: Model) -> Model:
        pass

    @abstractmethod
    def update(self, id: int, model: Model) -> Model:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> int:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Model:
        pass

    @abstractmethod
    def find_all(self, broker_type: Optional[BrokerType] = None) -> List[Model]:
        pass

    @abstractmethod
    def upsert_all(self, models: List[Model]) -> List[Model]:
        pass
