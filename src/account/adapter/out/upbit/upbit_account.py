from time import sleep
import time
from typing import Dict, override
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

    @override
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

    @override
    def sell_all(self, ticker: str) -> None:
        holdings: Dict[str, HoldingsInfo] = self.get_holdings()

        if ticker not in holdings:
            return

        sold_quantity = holdings[ticker].quantity
        self.sell_market_order(Ticker(ticker), sold_quantity)

    @override
    def buy_limit_order(self, ticker: Ticker, price: float, quantity: float):
        result = self.upbit.buy_limit_order(ticker.value, price, quantity)

        if isinstance(result, dict) and "error" in result.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_ORDER, result.get("error"))

        return result

    @override
    def buy_market_order(self, ticker: Ticker, quantity: float | None = None, price: float | None = None):
        ticker.validate_crypto_ticker()
        result = self.upbit.buy_market_order(ticker.value, price)

        if isinstance(result, dict) and "error" in result.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_ORDER, result.get("error"))

        return result

    @override
    def sell_market_order(self, ticker: Ticker, quantity: float) -> None:
        ticker.validate_crypto_ticker()
        self.upbit.sell_market_order(ticker.value, quantity)

    @override
    def get_holdings(self, market: Market = Market.KR) -> Dict[str, HoldingsInfo]:
        return {
            f"{stock['unit_currency']}-{stock['currency']}": HoldingsInfo(
                name=stock["currency"],
                quantity=float(stock["balance"]),
                avg_price=float(stock["avg_buy_price"]),
                eval_amt=round(float(stock["balance"]) * float(stock["avg_buy_price"]), 4),
            )
            for stock in self._get_balances()
            if stock["currency"] != "KRW"  # KRW는 제외
        }

    @override
    def get_total_principal(self) -> float:
        total_principal = 0.0
        balances = self._get_balances()
        for balance in balances:
            if balance["currency"] == "KRW":
                total_principal += float(balance["balance"])
            else:
                total_principal += float(balance["balance"]) * float(balance["avg_buy_price"])
        return total_principal

    @override
    def get_revenue(self) -> float:
        balance = self.get_balance()
        total_principal = self.get_total_principal()
        return (balance - total_principal) / total_principal

    def _get_balances(self) -> list[dict]:
        balances = self.upbit.get_balances()

        if isinstance(balances, dict) and "error" in balances.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, balances.get("error"))

        return balances

    @override
    def sell_all_holdings(self) -> None:
        holdings: Dict[str, HoldingsInfo] = self.get_holdings()
        for ticker, holdings_info in holdings.items():
            time.sleep(0.03)
            self.sell_market_order(Ticker(ticker), holdings_info.quantity)
