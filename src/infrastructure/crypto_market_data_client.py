from datetime import datetime, timedelta, date

import pytz
from pandas import DataFrame

import src.infrastructure.exchange.upbit_client as upbit_client
from src.infrastructure.exchange.interval import Interval
from src.infrastructure.timezone import TimeZone


class CryptoMarketDataClient:
    """
    시장 데이터 조회 클라이언트
    """

    def get_ohlcv(self, ticker: str, interval: Interval, count: int) -> DataFrame:
        # TODO: 날짜, 종목 별로 캐시
        return DataFrame()

    def get_last_day_hourly_ohlcv(self, ticker: str, tz: TimeZone = TimeZone.UTC_P9) -> DataFrame:
        """
        해당 타임존의 '어제' 60분봉 데이터 조회
        """
        yesterday: date = self._get_yesterday(tz)
        df: DataFrame = upbit_client.get_ohlcv(ticker, interval=Interval.M60, count=48)
        return df[yesterday == df.index.date]

    def _get_yesterday(self, tz: TimeZone) -> date:
        return datetime.now(pytz.UTC).astimezone(pytz.timezone(tz)).date() - timedelta(days=1)

    # 거래대금 상위 N개 종목 조회
    def get_top_n_volume_tickers(self, n: int = 5) -> list[str]:
        # TODO: 날짜 별로 캐시
        pass
