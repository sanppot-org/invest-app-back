from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

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
    def find_all(self) -> List[Model]:
        pass
