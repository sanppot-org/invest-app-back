from typing import Dict
from src.account.holdings import Holdings
from src.account.account import Account
from src.infrastructure.exchange_client import ExchangeClient


class AccountOperator:
    def __init__(self, account: Account, exchange_client: ExchangeClient):
        self.account = account
        self.exchange_client = exchange_client

    def get_balance(self) -> float:
        return self.exchange_client.get_balance()

    def get_holdings(self) -> Dict[str, Holdings]:
        return self.exchange_client.get_holdings()
