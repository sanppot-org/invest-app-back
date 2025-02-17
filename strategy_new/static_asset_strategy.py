from datetime import datetime
from re import L
from typing import Dict, List, Optional, override

from src.account.domain.account import Account
from src.account.domain.holdings import HoldingsInfo
from src.common.domain.ticker import Ticker
from src.strategy.domain.interval import Interval
from strategy_new.strategy import Strategy


class StaticAssetStrategy(Strategy):
    def __init__(
        self,
        name: str,
        account: Account,
        allocation: float,
        tickers: List[Ticker],
        interval: Interval,
        last_run: Optional[datetime] = None,
    ):
        super().__init__(
            name,
            account,
            allocation,
            tickers,
            last_run,
        )
        self.interval = interval

    @override
    def should_trade(self) -> bool:
        # 첫 실행인 경우 실행
        if self.last_run is None:
            return True

        current_time = datetime.now()
        return self.interval.is_time_to_rebalance(current_time, self.last_run)

    @override
    def should_buy(self, ticker: Ticker) -> bool:
        # 해당 종목이 없는 경우 매수
        holdings: Dict[str, HoldingsInfo] = self.account.get_holdings()
        if ticker.value not in holdings:
            return True

        # 해당 종목의 평가금액이 할당금액보다 한 주 이상 부족한 경우 매수
        balance = self.account.get_balance()
        allocation_amount = balance * self.allocation

        holding = holdings[ticker.value]
        if holding.eval_amt < allocation_amount:
            return True

        return False

    @override
    def should_sell(self, ticker: Ticker) -> bool:
        return False

    @override
    def buy(self, ticker: Ticker, allocation_amount: float):
        pass

    @override
    def sell(self, ticker: Ticker, allocation_amount: float):
        pass

    @override
    def get_buy_weight(self, ticker: Ticker) -> float:
        return 1

    @override
    def get_sell_weight(self, ticker: Ticker) -> float:
        return 0
