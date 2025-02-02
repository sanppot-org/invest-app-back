from datetime import datetime, timedelta

import pytz


class TimeUtil:
    def __init__(self, timezone: str):
        self.timezone = timezone

    def get_current_time(self):
        """
        원하는 타임존의 현재 시간 조회
        """
        return datetime.now(tz=pytz.timezone(self.timezone))

    def is_morning(self) -> bool:
        """
        현재 시간이 오전인지 확인
        """
        is_morning = self.get_current_time().hour < 12
        return is_morning

    def is_afternoon(self) -> bool:
        """
        현재 시간이 오후인지 확인
        """

        is_afternoon = self.get_current_time().hour >= 12
        return is_afternoon

    def get_today(self):
        """
        오늘 날짜 조회
        """

        return self.get_current_time().date()

    def get_yesterday(self):
        """
        어제 날짜 조회
        """

        return self.get_today() - timedelta(days=1)

    def get_twenty_days_ago(self):
        """
        20일 전 날짜 조회
        """

        return self.get_today() - timedelta(days=20)
