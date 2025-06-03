from datetime import datetime
from typing import Any, Optional

import pandas as pd
import pytz
import requests
from pandas import DataFrame

from src.infrastructure.exchange.interval import Interval
from src.infrastructure.timezone import TimeZone

_UTC: str = "UTC"
_MAX_CALL_COUNT: int = 200
_UTC_COLUMN_NAME: str = "candle_date_time_utc"
_ohlcv_url: dict = {
    Interval.DAY: "https://api.upbit.com/v1/candles/days",
    Interval.M1: "https://api.upbit.com/v1/candles/minutes/1",
    Interval.M3: "https://api.upbit.com/v1/candles/minutes/3",
    Interval.M5: "https://api.upbit.com/v1/candles/minutes/5",
    Interval.M10: "https://api.upbit.com/v1/candles/minutes/10",
    Interval.M15: "https://api.upbit.com/v1/candles/minutes/15",
    Interval.M30: "https://api.upbit.com/v1/candles/minutes/30",
    Interval.M60: "https://api.upbit.com/v1/candles/minutes/60",
    Interval.M240: "https://api.upbit.com/v1/candles/minutes/240",
    Interval.WEEK: "https://api.upbit.com/v1/candles/weeks",
    Interval.MONTH: "https://api.upbit.com/v1/candles/months",
}
_df_columns: dict[str, str] = {
    "candle_date_time_utc": "",
    "opening_price": "open",
    "high_price": "high",
    "low_price": "low",
    "trade_price": "close",
    "candle_acc_trade_volume": "volume",
    "candle_acc_trade_price": "value",
}


def get_ohlcv(
        ticker: str = "KRW-BTC",
        interval: Interval = Interval.DAY,
        count: int = 1,
        to: Optional[datetime] = None,
        tz: TimeZone = TimeZone.UTC_P9,
) -> DataFrame:
    """
    최대 갯수: 200
    """
    count = min(count, _MAX_CALL_COUNT)
    contents: list[dict] = _call(url=_get_url_ohlcv(interval), market=ticker, count=count, to=_date_to_str(to)).json()
    return _make_df(contents, tz)


def _make_df(contents: list[dict], tz: TimeZone) -> DataFrame:
    """
    [
        {
            "market": "KRW-BTC",
            "candle_date_time_utc": "2025-05-24T01:00:00",
            "candle_date_time_kst": "2025-05-24T10:00:00",
            "opening_price": 149962000.0,
            "high_price": 152700000.0,
            "low_price": 149422000.0,
            "trade_price": 150660000.0,
            "timestamp": 1748131199127,
            "candle_acc_trade_price": 160626638206.7191,
            "candle_acc_trade_volume": 1063.00688169,
            "prev_closing_price": 149878000.0,
            "change_price": 782000.0,
            "change_rate": 0.005217577,
        }
    ]

    위 형태의 JSON 데이터를 아래와 같은 형태의 DataFrame으로 변환

                        open	    high	    low	        close	    volume	       value               is_morning
    2025-05-24 01:00:00	149962000.0	152700000.0	149422000.0	150660000.0	1063.00688169  160626638206.7191   True
    """
    df = pd.DataFrame(data=contents, columns=list(_df_columns.keys()))
    df.set_index(_UTC_COLUMN_NAME, inplace=True)
    df.rename(columns=_df_columns, inplace=True)
    df.index = pd.to_datetime(df.index).tz_localize(_UTC).tz_convert(pytz.timezone(tz))
    df["is_morning"] = df.index.hour < 12
    return df


def _date_to_str(to) -> Optional[str]:
    if to:
        return to.strftime("%Y-%m-%d %H:%M:%S")
    return None


def _call(url: str, **params: Any):
    return requests.get(url, params=params)


def _get_url_ohlcv(interval: Interval = Interval.DAY):
    return _ohlcv_url[interval]
