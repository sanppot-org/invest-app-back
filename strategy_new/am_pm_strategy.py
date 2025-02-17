from datetime import datetime
from typing import List, Optional, override

import pytz
from src.account.domain.account import Account
from src.common.domain.ticker import Ticker
from strategy_new.df_holder_cache.df_holder_cache import DfHolderCache
from strategy_new.strategy import Strategy


class AMPMStrategy(Strategy):
    def __init__(
        self,
        name: str,
        account: Account,
        allocation: float,  # 전략 할당 비중 (0~1)
        tickers: List[Ticker],
        df_holder_cache: DfHolderCache,
        timezone: str,
        target_volatility: float,
        last_run: Optional[datetime] = None,
    ):
        super().__init__(name, account, allocation, tickers, last_run)
        self.target_volatility = target_volatility
        self.timezone = pytz.timezone(timezone)
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
        # 매수 조건 : 오전 and 전일 오후 수익률 > 0 and 전일 오후 거래량 > 전일 오전 거래량

        # 오전
        current_time = datetime.now(self.timezone)
        if current_time.hour >= 12:
            return False

        # 전일 오후 수익률 > 0
        df_holder = self.df_holder_cache.get_holder(ticker.value)
        yesterday_afternoon_close = df_holder.df_yesterday_afternoon["close"].values[0]
        yesterday_afternoon_open = df_holder.df_yesterday_afternoon["open"].values[0]
        yesterday_afternoon_return = (yesterday_afternoon_close - yesterday_afternoon_open) / yesterday_afternoon_open
        if yesterday_afternoon_return <= 0:
            return False

        # 전일 오후 거래량 > 전일 오전 거래량
        yesterday_morning_volume = df_holder.df_yesterday_morning["volume"].values[0]
        yesterday_afternoon_volume = df_holder.df_yesterday_afternoon["volume"].values[0]
        return yesterday_afternoon_volume > yesterday_morning_volume

    @override
    def should_sell(self, ticker: Ticker) -> bool:
        # 매도 조건 : 오후
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

        # 전일 오전 변동성
        yesterday_morning_high = df_holder.df_yesterday_morning["high"].values[0]
        yesterday_morning_low = df_holder.df_yesterday_morning["low"].values[0]
        yesterday_morning_range = yesterday_morning_high - yesterday_morning_low
        yesterday_morning_open = df_holder.df_yesterday_morning["open"].values[0]
        yesterday_morning_volatility = yesterday_morning_range / yesterday_morning_open

        # 매수 비중
        buy_weight = min(1, self.target_volatility / yesterday_morning_volatility)

        return buy_weight
