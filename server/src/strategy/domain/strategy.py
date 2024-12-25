from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from src.common.domain.base_domain_model import BaseDomainModel
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import Market
from src.strategy.domain.interval import Interval
from src.strategy.domain.stock_info import StockInfo


@dataclass
class Strategy(BaseDomainModel):
    id: Optional[int]
    name: str
    invest_rate: float
    market: Market
    stocks: Dict[str, StockInfo]
    interval: Interval
    last_run: Optional[datetime]
    account_id: int
    is_active: bool

    def validate_portfolio_rate(self):
        if sum([stock.target_rate for stock in self.stocks.values()]) != 1:
            raise InvestAppException(
                ExeptionType.INVALID_PORTFOLIO_RATE,
                {ticker: stock.target_rate for ticker, stock in self.stocks.items()},
            )

    def get_invest_amount(self, balance: float) -> float:
        return balance * self.invest_rate

    def get_stocks(self) -> Dict[str, StockInfo]:
        return self.stocks

    def complete_rebalance(self):
        self.last_run = datetime.now()

    # TODO: 고도화 하기.
    def is_time_to_rebalance(self, now: datetime):
        if self.last_run is None:
            return

        interval: Interval = self.interval
        if interval.is_month():
            this_month = now.month
            if this_month in interval.values and not now.month == self.last_run.month:
                return

        # TODO: 다른 조건 추가하기

        raise InvestAppException(exception_type=ExeptionType.NOT_TIME_TO_REBALANCE)

    def get_market(self) -> Market:
        return self.market

    def get_account_id(self) -> int:
        return self.account_id
