from datetime import datetime
from turtle import pu
from typing import List, Optional, override

import numpy as np
import pytz
from src.account.domain.account import Account
from src.common.domain.ticker import Ticker
from strategy_new.df_holder_cache.df_holder_cache import DfHolderCache
from strategy_new.strategy import Strategy


class VolStrategy(Strategy):
    def __init__(
        self,
        account: Account,
        allocation: float,  # 전략 할당 비중 (0~1)
        tickers: List[Ticker],
        target_volatility: float,
        timezone: str,
        df_holder_cache: DfHolderCache,
        buy_weight: Optional[float] = None,
        target_price: Optional[float] = None,  # 돌파 기준 가격
        last_run: Optional[datetime] = None,
    ):
        super().__init__(
            "변동성 돌파 전략",
            account,
            allocation,
            tickers,
            last_run,
        )
        self.timezone = pytz.timezone(timezone)
        self.target_volatility = target_volatility
        self.buy_weight = buy_weight
        self.target_price = target_price
        self.df_holder_cache = df_holder_cache

    @override
    def should_trade(self) -> bool:
        # 첫 실행인 경우 실행
        if self.last_run is None:
            return True

        current_time = datetime.now(self.timezone)

        is_same_day = self.last_run.date() == current_time.date()
        is_same_period = (current_time.hour < 12) == (self.last_run.hour < 12)

        # 같은 날 같은 시간대가 아니면 실행
        return not (is_same_day and is_same_period)

    @override
    def should_buy(self, ticker: Ticker) -> bool:
        # 오전
        current_time = datetime.now(self.timezone)
        if current_time.hour >= 12:
            return False

        # 매수 비중 > 0
        if self.get_buy_weight(ticker) <= 0:
            return False

        # 현재가 > 돌파 기준 가격
        current_price = float(pu.get_current_price(ticker))
        return current_price > self._get_breakout_price(ticker)

    @override
    def should_sell(self, ticker: Ticker) -> bool:
        current_time = datetime.now(self.timezone)
        return current_time.hour >= 12

    @override
    def buy(self, ticker: Ticker, allocation_amount: float):
        self.account.buy_market_order(ticker, allocation_amount)
        self.last_run = datetime.now(self.timezone)

    @override
    def sell(self, ticker: Ticker, allocation_amount: float):
        self.account.sell_all(ticker.value)
        self.last_run = datetime.now(self.timezone)

    @override
    def get_buy_weight(self, ticker: Ticker) -> float:
        df_holder = self.df_holder_cache.get_holder(ticker.value)

        if not self.buy_weight:
            # 전일 오전 변동성
            yesterday_morning_high = df_holder.df_yesterday_morning["high"].values[0]
            yesterday_morning_low = df_holder.df_yesterday_morning["low"].values[0]
            yesterday_morning_range = yesterday_morning_high - yesterday_morning_low
            yesterday_morning_open = df_holder.df_yesterday_morning["open"].values[0]
            yesterday_morning_volatility = yesterday_morning_range / yesterday_morning_open

            # 오전 이동평균 스코어 평균
            yesterday_close = df_holder.df_yesterday_afternoon["close"].values[0]
            ma_periods = [3, 5, 10, 20]
            scores = [(df_holder.df_morning[f"ma{p}"].values[0] < yesterday_close).astype(int) for p in ma_periods]
            ma_score = float(np.mean(scores))

            self.buy_weight = (self.target_volatility * yesterday_morning_volatility) / ma_score

        return self.buy_weight

    def _get_breakout_price(self, ticker: Ticker) -> float:
        """
        돌파 기준 가격 설정
        돌파 기준 가격 : 당일 시가(0시) + 전일 오전 레인지 * 20일 노이즈 비율 평균
        """
        df_holder = self.df_holder_cache.get_holder(ticker.value)

        if not self.target_price:
            # 당일 시가(0시)
            today_open = df_holder.df_yesterday_afternoon["close"].values[0]
            # 전일 오전 레인지
            yesterday_morning_high = df_holder.df_yesterday_morning["high"].values[0]
            yesterday_morning_low = df_holder.df_yesterday_morning["low"].values[0]
            yesterday_morning_range = yesterday_morning_high - yesterday_morning_low

            recent_20_days_noise_mean = df_holder.df_morning["noise"].mean()

            self.target_price = float(today_open + yesterday_morning_range * recent_20_days_noise_mean)
        return self.target_price
