from dataclasses import dataclass
import time
from typing import Dict, override
from src.account.domain.account import Account
from src.common.adapter.out import slack_noti_client
from src.common.adapter.out.upbit_df_holder import UpbitDfHolder
from src.common.domain.time_util import TimeUtil
from src.strategy.domain.coin.am_pm import AmPmStrategy
from src.strategy.domain.coin.sub_strategy import SubStrategy
from src.strategy.domain.strategy import Strategy
from src.strategy.domain.coin.volatility_breakout import VolatilityBreakoutStrategy
from src.common.domain.logging_config import logger

import pyupbit as pu


@dataclass
class CoinStrategy(Strategy):
    timezone: str
    coin_count: int

    @override
    def trade(self, account: Account):
        slack_noti_client.send_debug_noti(f"=== {self.name} 전략 실행 ===")
        self.do_trade(account)
        slack_noti_client.send_debug_noti(f"=== {self.name} 전략 종료 ===")

    def do_trade(self, account: Account):
        time_util = TimeUtil(self.timezone)
        current_time = time_util.get_current_time()

        slack_noti_client.send_debug_noti(
            f"last_run: {self.last_run},\n" f"current_time: {current_time}",
        )

        # 날이 바뀌지 않았으면 종료
        if self.last_run is not None and current_time.date() == self.last_run.date():
            return

        # 전략 할당 금액
        allocated_balance = account.get_balance()
        invest_amount = allocated_balance * self.invest_rate
        # 코인 별 할당 금액
        invest_amount_per_coin = invest_amount / self.coin_count

        slack_noti_client.send_debug_noti(
            f"allocated_balance: {allocated_balance},\n"
            f"invest_rate: {self.invest_rate},\n"
            f"invest_amount: {invest_amount},\n"
            f"coin_count: {self.coin_count},\n"
            f"invest_amount_per_coin: {invest_amount_per_coin}",
        )

        # 매수할 코인 목록 조회
        ticker_list = self.get_top_trade_volume_coin_list()

        slack_noti_client.send_debug_noti(f"거래할 코인 목록: {ticker_list}")

        # 오전/오후 전략 생성
        am_pm_strategy = AmPmStrategy(time_util=time_util)
        # 변동성 돌파 전략 생성
        volatility_breakout_strategy = VolatilityBreakoutStrategy(time_util=time_util)

        symbols: Dict[str, Symbol] = {}

        # 종목 생성
        for ticker in ticker_list:
            time.sleep(0.05)
            symbol = Symbol(ticker, invest_amount_per_coin, self.timezone)
            symbol.add_sub_strategy(am_pm_strategy)
            symbol.add_sub_strategy(volatility_breakout_strategy)
            symbols[ticker] = symbol

        for symbol in symbols.values():
            symbol.trade(account)

        self.last_run = time_util.get_current_time()

    def update(self, strategy: "CoinStrategy"):
        super().update(strategy)
        self.timezone = strategy.timezone
        self.coin_count = strategy.coin_count

    def get_top_trade_volume_coin_list(self) -> list[str]:
        """
        최근 거래대금 상위 N개의 코인 리스트를 반환한다.
        """

        tickers: list[str] = list(pu.get_tickers("KRW"))

        trade_volumes: dict[str, float] = {}

        for ticker in tickers:
            time.sleep(0.05)
            ohlcv = pu.get_ohlcv(ticker, count=3)
            trade_volumes[ticker] = (ohlcv["close"] * ohlcv["volume"]).sum()

        return [ticker for ticker, _ in sorted(trade_volumes.items(), key=lambda x: x[1], reverse=True)[: self.coin_count]]


class Symbol:
    """종목 클래스"""

    def __init__(self, ticker: str, amount: float, timezone: str):
        self.ticker = ticker
        self.amount = amount
        self.upbit_df_holder = UpbitDfHolder(ticker, timezone)
        self.sub_strategies: list[SubStrategy] = []

    def add_sub_strategy(self, strategy: SubStrategy):
        """세부 전략 추가"""
        self.sub_strategies.append(strategy)

    def trade(self, account: Account):
        amount = self.amount / len(self.sub_strategies)
        for sub_strategy in self.sub_strategies:
            sub_strategy.trade(account, self.ticker, amount, self.upbit_df_holder)
