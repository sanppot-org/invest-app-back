from abc import abstractmethod
from typing import Generic

from src.common.infra.type import D, E


class EntityMapper(Generic[D, E]):
    @abstractmethod
    def to_entity(self, domain: D) -> E:
        pass

    @abstractmethod
    def to_domain(self, entity: E) -> D:
        pass
