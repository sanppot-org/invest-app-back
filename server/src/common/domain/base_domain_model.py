from abc import ABC, abstractmethod


class BaseDomainModel(ABC):
    def get_update_fields(self, exclude_keys: list[str] = []) -> dict:
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_") and key not in ["id"] and key not in exclude_keys}
