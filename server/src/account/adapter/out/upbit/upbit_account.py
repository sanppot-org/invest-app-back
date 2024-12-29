from time import sleep
from typing import Dict
import pyupbit
from pyupbit import Upbit

from src.account.domain.account import Account
from src.account.domain.account_info import AccountInfo
from src.account.domain.holdings import HoldingsInfo
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import Market
from src.common.domain.ticker import Ticker


class UpbitAccount(Account):
    def __init__(self, account_info: AccountInfo):
        super().__init__(account_info=account_info)
        self.upbit = Upbit(access=self.account_info.app_key, secret=self.account_info.secret_key)

    def get_balance(self, market: Market = Market.KR) -> float:
        stocks: list[dict] = self._get_balances()
        total_balance = 0.0

        for stock in stocks:
            if stock["currency"] == "KRW":
                total_balance += float(stock["balance"])
            else:
                sleep(0.1)
                current_price = float(pyupbit.get_current_price(f"KRW-{stock['currency']}"))
                total_balance += current_price * float(stock["balance"])

        return float(total_balance)

    def buy_market_order(self, ticker: Ticker, quantity: int) -> None:
        self.upbit.buy_market_order(ticker.value, quantity)

    def sell_market_order(self, ticker: Ticker, quantity: int) -> None:
        self.upbit.sell_market_order(ticker.value, quantity)

    def get_holdings(self, market: Market = Market.KR) -> Dict[Ticker, HoldingsInfo]:
        return {
            Ticker(stock["currency"]): HoldingsInfo(
                name=stock["currency"],
                quantity=float(stock["balance"]),
                avg_price=float(stock["avg_buy_price"]),
                eval_amt=round(float(stock["balance"]) * float(stock["avg_buy_price"]), 4),
            )
            for stock in self._get_balances()
        }

    def _get_balances(self) -> list[dict]:
        balances: dict | list = self.upbit.get_balances()

        if isinstance(balances, dict) and "error" in balances.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, balances.get("error"))

        return balances
