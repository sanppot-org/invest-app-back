from typing import Dict, Optional

from src.account.account import Account
from src.account.holdings import Holdings
from src.common.exception import InvestAppException, ExeptionType
from src.infrastructure.exchange.balance import Balance
from src.infrastructure.exchange.exchange_client import ExchangeClient


class AccountOperator:
    def __init__(self, account: Account, exchange_client: ExchangeClient):
        self.account = account
        self.exchange_client = exchange_client

    def get_balance(self) -> float:
        return self.exchange_client.get_balance().balance

    def get_holdings(self) -> Dict[str, Holdings]:
        return self.exchange_client.get_holdings()

    def sell_all(self):
        """
        전량 매도
        """
        self.exchange_client.sell_all()

    def buy_market_order(
            self,
            ticker: str,
            amount: Optional[float] = None,
            weight: Optional[float] = None,
    ):
        """
        시장가 매수

        amount, weight 둘 다 있는 경우 amount를 우선함

        amount: 매수 금액
        weight: 매수 비중 - 계좌의 전체 잔고에서 비중만큼 매수
        """
        if (amount is None) and (weight is None):
            raise InvestAppException(ExeptionType.ILLEGAL_ARGUMENT, amount=amount, weight=weight)

        if amount:
            self.exchange_client.buy_market_order(ticker, amount)
            return

        # 계좌 전체 잔고와 현재 매수 가능 금액을 가져와서, min((잔고 * weight), 매수 가능 금액)만큼 매수
        balance: Balance = self.exchange_client.get_balance()
        amount = min(balance.balance * weight, balance.buyable_amount)
        self.exchange_client.buy_market_order(ticker, amount)
