from datetime import datetime
from src.common.domain.type import Market


def test_is_market_open_before_open_time():
    """평일, 오픈 시간 전이라면 False를 반환한다."""
    date = datetime(2024, 12, 25, 8, 59, 0)  # 수요일
    assert Market.KR._is_market_open_time(date) is False


def test_is_market_open_after_open_time():
    """평일, 오픈 시간 후라면 False를 반환한다."""
    date = datetime(2024, 12, 25, 15, 26, 0)  # 수요일
    assert Market.KR._is_market_open_time(date) is False


def test_is_market_open_on_open_time2():
    """평일, 오픈 시간이라면 True를 반환한다."""
    date = datetime(2024, 12, 25, 9, 0, 0)  # 수요일
    assert Market.KR._is_market_open_time(date) is True

    date = datetime(2024, 12, 25, 12, 26, 0)  # 수요일
    assert Market.KR._is_market_open_time(date) is True

    date = datetime(2024, 12, 25, 15, 25, 0)  # 수요일
    assert Market.KR._is_market_open_time(date) is True


def test_is_market_open_on_open_time():
    """평일이라면 True를 반환한다."""

    monday = datetime(2024, 12, 16, 9, 0, 0)  # 월요일
    tuesday = datetime(2024, 12, 17, 9, 0, 0)  # 화요일
    wednesday = datetime(2024, 12, 18, 9, 0, 0)  # 수요일
    thursday = datetime(2024, 12, 19, 9, 0, 0)  # 목요일
    friday = datetime(2024, 12, 20, 9, 0, 0)  # 금요일

    assert Market.KR._is_market_open_time(monday) is True
    assert Market.KR._is_market_open_time(tuesday) is True
    assert Market.KR._is_market_open_time(wednesday) is True
    assert Market.KR._is_market_open_time(thursday) is True
    assert Market.KR._is_market_open_time(friday) is True


def test_is_market_open_on_weekend():
    """주말이라면 False를 반환한다."""
    saturday = datetime(2024, 12, 28, 9, 0, 0)  # 토요일
    assert Market.KR._is_market_open_time(saturday) is False

    sunday = datetime(2024, 12, 29, 9, 0, 0)  # 일요일
    assert Market.KR._is_market_open_time(sunday) is False
