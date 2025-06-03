from datetime import datetime, timezone

import pytest

from src.strategy.strategy import Strategy


@pytest.fixture
def strategy_data():
    return {
        "id": 1,
        "name": "Test Strategy",
        "account_id": 100,
        "last_executed_at": datetime.now(timezone.utc),
        "tz_offset": 9,
        "target_volatility": 0.01,
        "is_active": True,
        "tickers": ["AAPL", "GOOGL"],
    }


def test_strategy_creation(strategy_data):
    strategy = Strategy(**strategy_data)

    assert strategy.id == strategy_data["id"]
    assert strategy.name == strategy_data["name"]
    assert strategy.account_id == strategy_data["account_id"]
    assert strategy.tz_offset == strategy_data["tz_offset"]
    assert strategy.target_volatility == strategy_data["target_volatility"]
    assert strategy.is_active == strategy_data["is_active"]
    assert strategy.tickers == strategy_data["tickers"]


def test_strategy_validation():
    with pytest.raises(AssertionError):
        Strategy(id=1, name="", account_id=100, last_executed_at=datetime.now(timezone.utc))  # 빈 이름


def test_strategy_update(strategy_data):
    strategy = Strategy(**strategy_data)
    updated_data = strategy_data.copy()
    updated_data["name"] = "Updated Strategy"
    updated_data["target_volatility"] = 0.02

    updated_strategy = Strategy(**updated_data)
    strategy.update(updated_strategy)

    assert strategy.name == "Updated Strategy"
    assert strategy.target_volatility == 0.02
