from dataclasses import dataclass
from datetime import datetime
from typing import Dict, override
from src.account.domain.account import Account
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import Market
from src.strategy.domain.interval import Interval
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy_info import StrategyInfo


@dataclass
class StaticAssetStrategy(StrategyInfo):
    market: Market
    stocks: Dict[str, StockInfo]
    interval: Interval

    @override
    def validate(self):
        if sum([stock.target_rate for stock in self.stocks.values()]) != 1:
            raise InvestAppException(
                ExeptionType.INVALID_PORTFOLIO_RATE,
                {ticker: stock.target_rate for ticker, stock in self.stocks.items()},
            )

    @override
    def trade(self, account: Account):
        pass

    def buy(self, account: Account):
        pass

    def sell(self, account: Account):
        pass

    def get_stocks(self) -> Dict[str, StockInfo]:
        return self.stocks

    def check_is_time_to_rebalance(self, now: datetime):
        self.interval.is_time_to_rebalance(now, self.last_run)

    def get_market(self) -> Market:
        return self.market

    def update(self, strategy: "StaticAssetStrategy"):
        super().update(strategy)
        self.market = strategy.market
        self.stocks = strategy.stocks
        self.interval = strategy.interval
