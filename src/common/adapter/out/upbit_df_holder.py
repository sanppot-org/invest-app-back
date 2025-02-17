import numpy as np
import pandas as pd
from src.common.domain.logging_config import logger
from src.common.adapter.out import upbit_util
from src.common.domain.time_util import TimeUtil


class UpbitDfHolder:
    def __init__(self, ticker: str, timezone: str):
        self.ticker = ticker
        self.timezone = timezone
        self.time_util = TimeUtil(timezone)

        self.df_morning: pd.DataFrame
        self.df_afternoon: pd.DataFrame
        self.df_yesterday_morning: pd.DataFrame
        self.df_yesterday_afternoon: pd.DataFrame

        self.refresh_data()

    def refresh_data(self):
        df = upbit_util.get_ohlcv(ticker=self.ticker, interval="minute60", count=24 * 21, timezone=self.timezone)
        df_twenty_days_ago = self._filter_data(df)
        self.df_morning = self._process_morning_data(df_twenty_days_ago)
        self.df_afternoon = self._process_afternoon_data(df_twenty_days_ago)
        self.df_yesterday_morning = self.df_morning[self.df_morning.index == self.time_util.get_yesterday()]
        self.df_yesterday_afternoon = self.df_afternoon[self.df_afternoon.index == self.time_util.get_yesterday()]

    def _process_morning_data(self, df_twenty_days_ago: pd.DataFrame) -> pd.DataFrame:
        """
        오전 데이터 가공

        df : 최근 20일의 데이터
        """

        df_morning = df_twenty_days_ago[df_twenty_days_ago.index.hour < 12]
        agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
        df_morning_grouped = df_morning.groupby(df_morning.index.date).agg(agg)

        # 오전 데이터에 노이즈 추가
        df_morning_grouped["noise"] = 1 - abs(df_morning_grouped["close"] - df_morning_grouped["open"]) / (
            df_morning_grouped["high"] - df_morning_grouped["low"]
        )

        # 최근 3, 5, 10, 20일 오전 이동평균선 구하기
        df_morning_grouped["ma3"] = df_morning_grouped["close"].rolling(window=3).mean()
        df_morning_grouped["ma5"] = df_morning_grouped["close"].rolling(window=5).mean()
        df_morning_grouped["ma10"] = df_morning_grouped["close"].rolling(window=10).mean()
        df_morning_grouped["ma20"] = df_morning_grouped["close"].rolling(window=20).mean()

        return df_morning_grouped

    def _process_afternoon_data(self, df_twenty_days_ago: pd.DataFrame) -> pd.DataFrame:
        """
        오후 데이터 가공

        df : 최근 20일의 데이터
        """

        df_afternoon = df_twenty_days_ago[df_twenty_days_ago.index.hour >= 12]
        agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
        df_afternoon_grouped = df_afternoon.groupby(df_afternoon.index.date).agg(agg)
        return df_afternoon_grouped

    def _filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        20일 전 ~ 어제 날짜의 데이터만 필터링
        """

        return df[(df.index.date >= self.time_util.get_twenty_days_ago()) & (df.index.date <= self.time_util.get_yesterday())]

    def get_yesterday_close(self) -> float:
        """
        어제 오후 종가(= 오늘 오전 시가) 조회
        """

        return self.df_yesterday_afternoon["close"].values[0]
