from abc import ABC, abstractmethod
from typing import List, TypeVar


M = TypeVar("M")


class Repository[M](ABC):
    @abstractmethod
    def save(self, model: M) -> M:
        pass

    @abstractmethod
    def update(self, id: int, model: M) -> M:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> int:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> M | None:
        pass

    @abstractmethod
    def find_all(self) -> List[M]:
        pass
