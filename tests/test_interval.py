from datetime import datetime

import pytest
from src.common.domain.exception import InvestAppException
from src.common.domain.type import TimeUnit
from src.strategy.domain.interval import Interval


def test_check_is_time_to_rebalance_pass():
    """1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 1월이라면 아무 예외가 발생하지 않는다."""
    interval = Interval(time_unit=TimeUnit.MONTH, values=[1, 2, 3])
    interval.is_time_to_rebalance(now=datetime(2024, 2, 1), last_run=datetime(2024, 1, 1))


def test_check_is_time_to_rebalance_fail():
    """1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 2월이라면 예외가 발생한다."""
    interval = Interval(time_unit=TimeUnit.MONTH, values=[1, 2, 3])
    with pytest.raises(InvestAppException) as e:
        interval.is_time_to_rebalance(now=datetime(2024, 2, 1), last_run=datetime(2024, 2, 1))
    assert "리밸런싱 조건이 아닙니다." in e.value.message


def test_check_is_time_to_rebalance_last_run_is_none():
    """현재가 리밸런스 월이고 last_run이 None이라면 예외가 발생하지 않는다."""
    interval = Interval(time_unit=TimeUnit.MONTH, values=[1, 2, 3])
    interval.is_time_to_rebalance(now=datetime(2024, 2, 1), last_run=None)
