from typing import List

import pytz
from src.account.domain.account import Account
from src.common.adapter.out.upbit_df_holder import UpbitDfHolder
from src.common.domain.ticker import Ticker
from strategy_new.condition.strategy_condition import StrategyCondition
from strategy_new.strategy import Strategy


class VolStrategy(Strategy):
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

    def buy(self, ticker: Ticker, allocation_amount: float):
        target_price: float = self._get_breakout_price(upbit_df_holder)

        self.account.buy_limit_order(ticker, target_price, allocation_amount)

    def sell(self, ticker: Ticker, allocation_amount: float):
        self.account.sell_all(ticker.value)

    def calculate_buy_weight(self, ticker: Ticker) -> float:
        yesterday_morning_volatility = upbit_df_holder.get_yesterday_morning_volatility()
        calculated_ratio = min(1, self.target_volatility / yesterday_morning_volatility)

        return calculated_ratio * upbit_df_holder.calculate_ma_score(upbit_df_holder.get_yesterday_close())

    def calculate_sell_weight(self, ticker: Ticker) -> float:
        return 1

    def _get_breakout_price(self, upbit_df_holder: UpbitDfHolder) -> float:
        """
        돌파 기준 가격 설정
        돌파 기준 가격 : 당일 시가(0시) + 전일 오전 레인지 * 20일 노이즈 비율 평균
        """

        today_open = upbit_df_holder.get_yesterday_close()
        yesterday_morning_range = upbit_df_holder.get_yesterday_morning_range()
        recent_20_days_noise_mean = upbit_df_holder.get_recent_20_days_noise_mean()
        breakout_price = float(today_open + yesterday_morning_range * recent_20_days_noise_mean)
        return breakout_price
