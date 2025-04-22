from src.common.type import BrokerType
from src.infrastructure.exchange_client import ExchangeClient
from src.infrastructure.upbit_exchange_client import UpbitExchangeClient


class ExchangeClientFactory:
    def create(self, broker_type: BrokerType, app_key: str, secret_key: str) -> ExchangeClient:
        if broker_type == BrokerType.UPBIT:
            return UpbitExchangeClient(app_key, secret_key)
        else:
            raise ValueError(f"Unsupported broker type: {broker_type}")
