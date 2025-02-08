from typing import List

import pytz
from src.account.domain.account import Account
from src.common.domain.ticker import Ticker
from strategy_new.condition.strategy_condition import StrategyCondition
from strategy_new.strategy import Strategy


class AMPMStrategy(Strategy):
    def __init__(
        self,
        name: str,
        account: Account,
        allocation: float,  # 전략 할당 비중 (0~1)
        tickers: List[Ticker],
        trade_condition: StrategyCondition,
        buy_condition: StrategyCondition,
        sell_condition: StrategyCondition,
        target_volatility: float = 0.01,
        timezone: str = "Etc/GMT+11",
    ):
        super().__init__(name, account, allocation, tickers, trade_condition, buy_condition, sell_condition)
        self.target_volatility = target_volatility
        self.timezone = pytz.timezone(timezone)

    # def should_trade(self) -> bool:
    #     # 첫 실행 or 오늘 실행하지 않은 경우 or 오후에 실행하지 않은 경우
    #     return self.last_update is None or self.last_update.date() != datetime.now(self.timezone).date() or self.last_update.hour < 12

    def buy(self, ticker: Ticker, allocation_amount: float):
        self.account.buy_market_order(ticker, allocation_amount)

    def sell(self, ticker: Ticker, allocation_amount: float):
        self.account.sell_all(ticker.value)

    def calculate_buy_weight(self, ticker: Ticker) -> float:
        yesterday_morning_volatility = upbit_df_holder.get_yesterday_morning_volatility()
        calculated_ratio = min(1, self.target_volatility / yesterday_morning_volatility)

        return calculated_ratio

    def calculate_sell_weight(self, ticker: Ticker) -> float:
        return 1
