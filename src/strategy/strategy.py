from datetime import datetime, timezone

import pytz

from src.common.domain_model import DomainModel
from src.infrastructure.timezone import TimeZone
from src.strategy.strategy_type import StrategyType


class Strategy(DomainModel):
    def __init__(
            self,
            id: int,
            name: str,
            account_id: int,
            last_executed_at: datetime,
            type: StrategyType,
            tz: TimeZone = TimeZone.UTC_P9,
            target_volatility: float = 0.01,
            is_active: bool = True,
            tickers: list[str] = None,
    ):
        self.id = id
        self.name = name
        self.account_id = account_id
        self.last_executed_at = last_executed_at
        self.type = type
        self.tz = tz
        self.target_volatility = target_volatility
        self.is_active = is_active
        self.tickers = tickers

        self._validate()

    def update(self, strategy: "Strategy"):
        super().update(strategy)
        self._validate()

    def _validate(self):
        assert all([self.name, self.account_id, self.tz, self.type]), "필수 필드가 누락되었습니다"

    def is_last_execution_time_this_afternoon(self) -> bool:
        return self._is_last_execution_time_this_day() and self._get_last_execution_time().hour >= 12

    def is_last_execution_time_this_morning(self) -> bool:
        return self._is_last_execution_time_this_day() and self._get_last_execution_time().hour < 12

    def _is_last_execution_time_this_day(self) -> bool:
        return self._get_last_execution_time().date() == self._get_now().date()

    def _get_last_execution_time(self):
        return self.last_executed_at.astimezone(pytz.timezone(self.tz))

    def update_last_executed_at(self):
        self.last_executed_at = datetime.now(timezone.utc)

    def is_afternoon(self) -> bool:
        return self._get_now().hour >= 12

    def _get_now(self):
        return datetime.now(pytz.timezone(self.tz))
