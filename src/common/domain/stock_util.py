import pandas as pd
import pyupbit as pu
from src.common.domain.config import logger
import time


def get_ma(df: pd.DataFrame, period: int) -> pd.DataFrame:
    """
    이동평균선을 반환한다.
    """
    return df.rolling(period).mean()


def get_recent_trade_volume(ticker: str, df: pd.DataFrame) -> float:
    """
    최근 거래대금을 반환한다. (어제 + 오늘)
    """
    try:
        return float(df["close"][-1] * df["volume"][-1] + df["close"][-2] * df["volume"][-2])
    except Exception as e:
        logger.error(f"Error getting recent trade volume for {ticker}: {e}")
        return 0


def get_top_trade_volume_coin_list(interval: str, top_n: int) -> list[str]:
    """
    최근 거래대금 상위 N개의 코인 리스트를 반환한다.
    """
    tickers: list[str] = list(pu.get_tickers("KRW"))

    trade_volumes: dict[str, float] = {}
    for ticker in tickers:
        trade_volumes[ticker] = get_recent_trade_volume(ticker, pu.get_ohlcv(ticker, interval=interval, count=2))
        time.sleep(0.05)

    return [ticker for ticker, _ in sorted(trade_volumes.items(), key=lambda x: x[1], reverse=True)[:top_n]]
