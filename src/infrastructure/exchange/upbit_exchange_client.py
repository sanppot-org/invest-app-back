import time
from time import sleep
from typing import Dict, override

import pyupbit
from pyupbit import Upbit

from src.account.holdings import Holdings
from src.common.exception import ExeptionType, InvestAppException
from src.infrastructure.exchange.balance import Balance
from src.infrastructure.exchange.exchange_client import ExchangeClient

KRW = 'KRW'
CURRENCY = 'currency'
UNIT_CURRENCY = 'unit_currency'
BALANCE = 'balance'
AVG_BUY_PRICE = 'avg_buy_price'
ERROR = 'error'


class UpbitExchangeClient(ExchangeClient):
    """
    Upbit 클라이언트
    """

    def __init__(self, access_key: str, secret_key: str):
        self.upbit = Upbit(access_key, secret_key)

    @override
    def get_balance(self) -> Balance:
        buyable_amount = 0
        total_balance = 0.0
        stocks: list[dict] = self._get_balances()

        for stock in stocks:
            if stock[CURRENCY] == KRW:
                krw = float(stock[BALANCE])
                total_balance += krw
                buyable_amount = krw
            else:
                time.sleep(0.05)
                ticker = f"{stock[UNIT_CURRENCY]}-{stock[CURRENCY]}"
                current_price = float(pyupbit.get_current_price(ticker))
                total_balance += current_price * float(stock[BALANCE])

        return Balance(balance=total_balance, buyable_amount=buyable_amount)

    @override
    def get_holdings(self) -> Dict[str, Holdings]:
        return {
            f"{stock[UNIT_CURRENCY]}-{stock[CURRENCY]}": Holdings(
                name=stock[CURRENCY],
                code=f"{stock[UNIT_CURRENCY]}-{stock[CURRENCY]}",
                quantity=float(stock[BALANCE]),
                avg_price=float(stock[AVG_BUY_PRICE]),
                eval_amt=round(float(stock[BALANCE]) * float(stock[AVG_BUY_PRICE]), 4),
            )
            for stock in self._get_balances()
            if stock[CURRENCY] != KRW  # KRW는 제외
        }

    @override
    def buy_limit_order(self, ticker: str, limit_price: float, volume: float):
        if not ticker or not limit_price or not volume:
            raise InvestAppException(ExeptionType.ILLEGAL_ARGUMENT, ticker=ticker, limit_price=limit_price, volume=volume)

        result = self.upbit.buy_limit_order(ticker=ticker, price=limit_price, volume=volume)
        if isinstance(result, dict) and ERROR in result.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_ORDER, error=result.get(ERROR))
        return result

    @override
    def buy_market_order(self, ticker: str, amount: float):
        if not ticker or not amount:
            raise InvestAppException(ExeptionType.ILLEGAL_ARGUMENT, ticker=ticker, amount=amount)

        result = self.upbit.buy_market_order(ticker=ticker, price=amount)
        if isinstance(result, dict) and ERROR in result.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_ORDER, error=result.get(ERROR))
        return result

    @override
    def sell_market_order(self, ticker: str, amount: float):
        if not ticker or not amount:
            raise InvestAppException(ExeptionType.ILLEGAL_ARGUMENT, ticker=ticker, amount=amount)

        self.upbit.sell_market_order(ticker=ticker, volume=amount)

    @override
    def sell_limit_order(self, ticker: str, limit_price: float, volume: float):
        if not ticker or not limit_price or not volume:
            raise InvestAppException(ExeptionType.ILLEGAL_ARGUMENT, ticker=ticker, limit_price=limit_price, volume=volume)

        self.upbit.sell_limit_order(ticker=ticker, price=limit_price, volume=volume)

    @override
    def sell_all(self) -> None:
        holdings_dict: Dict[str, Holdings] = self.get_holdings()
        for ticker, holdings in holdings_dict.items():
            self.sell_market_order(ticker, holdings.quantity)
            sleep(0.05)

    def get_total_principal(self) -> float:
        total_principal = 0.0
        balances = self._get_balances()
        for balance in balances:
            if balance[CURRENCY] == KRW:
                total_principal += float(balance[BALANCE])
            else:
                total_principal += float(balance[BALANCE]) * float(balance[AVG_BUY_PRICE])
        return total_principal

    def get_revenue(self) -> float:
        balance = self.get_balance().balance
        total_principal = self.get_total_principal()
        return (balance - total_principal) / total_principal

    def _get_balances(self) -> list[dict]:
        balances = self.upbit.get_balances()

        if isinstance(balances, dict) and ERROR in balances.keys():
            raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, error=balances.get(ERROR))

        return balances

    # def sell_all_holdings(self) -> None:
    #     holdings: Dict[str, Holdings] = self.get_holdings()
    #     for ticker, holdings_info in holdings.items():
    #         time.sleep(0.05)
    #         self.sell_market_order(Ticker(ticker), holdings_info.quantity)
