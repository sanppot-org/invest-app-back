from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np

from strategy_new.df_holder_cache.df_holder_cache import DfHolderCache


class DataProvider(ABC):
    """기본 데이터 제공자 인터페이스"""

    def __init__(self, timezone: str):
        self.timezone = timezone
        self.df_cache = DfHolderCache.get_instance(timezone)


class VolatilityDataProvider(DataProvider):
    """변동성 데이터 제공자 인터페이스"""

    @abstractmethod
    def get_yesterday_morning_volatility(self, ticker: str) -> float:
        """전일 오전의 변동성을 반환"""
        pass

    @abstractmethod
    def get_morning_ma_scores(self, ticker: str, periods: List[int]) -> float:
        """지정된 기간의 오전 이동평균 스코어를 반환"""
        pass


class UpbitVolDataProvider(VolatilityDataProvider):
    """업비트 기반 변동성 데이터 제공자"""

    def get_yesterday_morning_volatility(self, ticker: str) -> float:
        df_holder = self.df_cache.get_holder(ticker)
        return df_holder.get_yesterday_morning_volatility()

    def get_morning_ma_scores(self, ticker: str) -> float:
        """
        오전 이동평균 스코어 평균

        전일 종가가 3, 5, 10, 20일 이동평균보다 크면 1, 작으면 0 해서 평균
        """

        df_holder = self.df_cache.get_holder(ticker)
        yesterday_close = df_holder.get_yesterday_close()

        ma_periods = [3, 5, 10, 20]
        scores = [(df_holder.df_morning[f"ma{p}"].values[0] < yesterday_close).astype(int) for p in ma_periods]

        return float(np.mean(scores))


class PriceDataProvider(DataProvider):
    """가격 데이터 제공자"""

    def get_yesterday_close(self, ticker: str) -> float:
        df_holder = self.df_cache.get_holder(ticker)
        return df_holder.get_yesterday_close()

    def get_yesterday_morning_range(self, ticker: str) -> float:
        df_holder = self.df_cache.get_holder(ticker)
        return df_holder.get_yesterday_morning_range()


class NoiseDataProvider(DataProvider):
    """노이즈 데이터 제공자"""

    def get_recent_noise_mean(self, ticker: str) -> float:
        df_holder = self.df_cache.get_holder(ticker)
        return df_holder.get_recent_20_days_noise_mean()
