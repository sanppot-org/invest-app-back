from datetime import datetime
from src.common.application.port.out.time_holder import TimeHolder


class TimeHolderImpl(TimeHolder):
    def get_now(self) -> datetime:
        return datetime.now()
