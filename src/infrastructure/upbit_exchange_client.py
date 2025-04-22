import time
from typing import Dict, override
import pyupbit
from pyupbit import Upbit

from src.common.exception import ExeptionType, InvestAppException
from src.holdings import Holdings
from src.infrastructure.exchange_client import ExchangeClient


class UpbitExchangeClient(ExchangeClient):
    """
    Upbit 클라이언트
    """

    def __init__(self, access_key: str, secret_key: str):
        self.upbit = Upbit(access_key, secret_key)

    @override
    def get_balance(self) -> float:
        total_balance = 0.0
        stocks: list[dict] = self._get_balances()

        for stock in stocks:
            if stock["currency"] == "KRW":
                total_balance += float(stock["balance"])
            else:
                time.sleep(0.05)
                ticker = f"{stock['unit_currency']}-{stock['currency']}"
                current_price = float(pyupbit.get_current_price(ticker))
                total_balance += current_price * float(stock["balance"])

        return float(total_balance)

    @override
    def get_holdings(self) -> Dict[str, Holdings]:
        return {
            f"{stock['unit_currency']}-{stock['currency']}": Holdings(
                name=stock["currency"],
                code=f"{stock['unit_currency']}-{stock['currency']}",
                quantity=float(stock["balance"]),
                avg_price=float(stock["avg_buy_price"]),
                eval_amt=round(float(stock["balance"]) * float(stock["avg_buy_price"]), 4),
            )
            for stock in self._get_balances()
            if stock["currency"] != "KRW"  # KRW는 제외
        }

    # def sell_all(self, ticker: str) -> None:
    #     holdings: Dict[str, HoldingsInfo] = self.get_holdings()

    #     if ticker not in holdings:
    #         return

    #     sold_quantity = holdings[ticker].quantity
    #     self.sell_market_order(Ticker(ticker), sold_quantity)

    # def buy_limit_order(self, ticker: Ticker, price: float, quantity: float):
    #     result = self.upbit.buy_limit_order(ticker.value, price, quantity)

    #     if isinstance(result, dict) and "error" in result.keys():
    #         raise InvestAppException(ExeptionType.FAILED_TO_ORDER, result.get("error"))

    #     return result

    # def buy_market_order(self, ticker: Ticker, quantity: float | None = None, price: float | None = None):
    #     ticker.validate_crypto_ticker()
    #     result = self.upbit.buy_market_order(ticker=ticker.value, price=price)

    #     if isinstance(result, dict) and "error" in result.keys():
    #         raise InvestAppException(ExeptionType.FAILED_TO_ORDER, result.get("error"))

    #     return result

    # def sell_market_order(self, ticker: Ticker, quantity: float) -> None:
    #     ticker.validate_crypto_ticker()
    #     self.upbit.sell_market_order(ticker.value, quantity)

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

    # def sell_all_holdings(self) -> None:
    #     holdings: Dict[str, Holdings] = self.get_holdings()
    #     for ticker, holdings_info in holdings.items():
    #         time.sleep(0.05)
    #         self.sell_market_order(Ticker(ticker), holdings_info.quantity)
