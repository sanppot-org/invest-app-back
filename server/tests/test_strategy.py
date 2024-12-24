from datetime import datetime
from src.common.domain.exception import InvestAppException
from src.strategy.domain.strategy import Strategy, Interval
from src.common.domain.type import Market, TimeUnit
import pytest


# 1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 1월이라면 아무 예외가 발생하지 않는다.
def test_is_time_to_rebalance():
    strategy = get_strategy(Interval(time_unit=TimeUnit.MONTH, values=[1, 2, 3]), datetime(2024, 1, 1))
    strategy.is_time_to_rebalance(datetime(2024, 2, 1))


# 1,2,3월에 실행해야하는 경우, 현재는 2월이고 마지막 실행이 2월이라면 예외가 발생한다.
def test_is_time_to_rebalance_false():
    strategy = get_strategy(Interval(time_unit=TimeUnit.MONTH, values=[1, 2, 3]), datetime(2024, 2, 1))
    with pytest.raises(InvestAppException) as e:
        strategy.is_time_to_rebalance(datetime(2024, 2, 1))
    assert e.value.message == "리밸런싱 조건이 아닙니다. {}"


def get_strategy(interval: Interval, last_run: datetime):
    return Strategy(
        id=None,
        name="name",
        interval=interval,
        last_run=last_run,
        market=Market.KR,
        invest_rate=0.1,
        stocks={},
        account_id=10,
        is_active=False,
    )
