from abc import ABC, abstractmethod
from typing import Generic, List

from src.common.adapter.out.persistence.type import Command, Model


class Repository(ABC, Generic[Command, Model]):
    @abstractmethod
    def save(self, command: Command) -> Model:
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
