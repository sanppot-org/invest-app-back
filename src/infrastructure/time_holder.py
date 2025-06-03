from abc import ABC, abstractmethod
from datetime import datetime

from src.infrastructure.timezone import TimeZone


class TimeHolder(ABC):
    @abstractmethod
    def get_now(self, timezone: TimeZone = TimeZone.UTC_P9) -> datetime:
        """
        현재 시간 조회
        """
        pass

    @abstractmethod
    def is_morning(self, timezone: TimeZone = TimeZone.UTC_P9) -> bool:
        """
        오전 확인
        """
        pass

    @abstractmethod
    def is_afternoon(self, timezone: TimeZone = TimeZone.UTC_P9) -> bool:
        """
        오후 확인
        """
        pass
