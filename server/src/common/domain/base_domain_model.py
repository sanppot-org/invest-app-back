from abc import ABC, abstractmethod


class BaseDomainModel(ABC):
    @abstractmethod
    def get_update_fields(self) -> dict:
        pass
