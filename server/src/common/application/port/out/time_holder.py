from abc import ABC, abstractmethod
from datetime import datetime


class TimeHolder(ABC):
    @abstractmethod
    def get_now(self) -> datetime:
        pass
