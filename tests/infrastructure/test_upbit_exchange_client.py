import pytest
from src.config.config import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY
from src.infrastructure.upbit_exchange_client import UpbitExchangeClient


@pytest.fixture
def upbit_client() -> UpbitExchangeClient:
    return UpbitExchangeClient(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)


class TestUpbitClient:
    def test_get_balance_success(self, upbit_client: UpbitExchangeClient):
        balance: float = upbit_client.get_balance()
        assert balance > 0
