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
        total_balance = 0.0
        stocks: list[dict] = self._get_balances()

        for stock in stocks:
            if stock["currency"] == "KRW":
                total_balance += float(stock["balance"])
            else:
                sleep(0.05)
                current_price = float(pyupbit.get_current_price(f"{stock['unit_currency']}-{stock['currency']}"))
                total_balance += current_price * float(stock["balance"])

        return float(total_balance)

    def buy_market_order(self, ticker: Ticker, quantity: int) -> None:
        ticker.validate_crypto_ticker()
        self.upbit.buy_market_order(ticker.value, quantity)

    def sell_market_order(self, ticker: Ticker, quantity: int) -> None:
        ticker.validate_crypto_ticker()
        self.upbit.sell_market_order(ticker.value, quantity)

    def get_holdings(self, market: Market = Market.KR) -> Dict[str, HoldingsInfo]:
        return {
            stock["currency"]: HoldingsInfo(
                name=stock["currency"],
                quantity=float(stock["balance"]),
                avg_price=float(stock["avg_buy_price"]),
                eval_amt=round(float(stock["balance"]) * float(stock["avg_buy_price"]), 4),
            )
            for stock in self._get_balances()
        }

    def get_total_principal(self) -> float:
        total_principal = 0.0
        balances = self._get_balances()
        for balance in balances:
            if balance["currency"] == "KRW":
                total_principal += float(balance["balance"])
            else:
                total_principal += float(balance["balance"]) * float(balance["avg_buy_price"])
        return total_principal

    def get_revenue(self) -> float:
        balance = self.get_balance()
        total_principal = self.get_total_principal()
        return (balance - total_principal) / total_principal

    def _get_balances(self) -> list[dict]:
        balances = self.upbit.get_balances()

        if isinstance(balances, dict) and "error" in balances.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, balances.get("error"))

        return balances
