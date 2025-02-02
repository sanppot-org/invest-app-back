import pandas as pd
import pyupbit as pu
from src.common.domain.logging_config import logger
import time
from datetime import timedelta


def get_ohlcv(ticker: str = "KRW-BTC", interval: str = "minute60", count: int = 24 * 21, timezone: str = "Etc/GMT+11"):
    """
    원하는 타임존의 최근 N일 ohlcv 조회
    """
    df = pu.get_ohlcv(ticker=ticker, interval=interval, count=count)
    df.index = df.index - timedelta(hours=9)
    df.index = df.index.tz_localize("UTC").tz_convert(timezone)
    return df


def get_rsi(df: pd.DataFrame, period: int = 14, st: int = -1) -> float:
    """
    RSI(Relative Strength Index) 계산

    Args:
        df: OHLCV DataFrame
        period: RSI 계산 기간 (기본값 14일)
        st: 마지막에서 몇 번째 값을 반환할지 (기본값 -1: 가장 최근)

    Returns:
        float: RSI 값 (0-100)
    """
    # 종가 기준 일간 변화량 계산
    delta = pd.to_numeric(df["close"].diff())

    # 상승폭과 하락폭 분리
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # 평균 상승폭과 하락폭 계산 (EMA 사용)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    # RS(Relative Strength) 계산
    rs = avg_gain / avg_loss

    # RSI 계산
    rsi = 100 - (100 / (1 + rs))

    # st 인덱스의 RSI 값 반환
    return float(rsi.iloc[st])


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
        return float(df["close"].iloc[-1] * df["volume"].iloc[-1] + df["close"].iloc[-2] * df["volume"].iloc[-2])
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
        time.sleep(0.05)
        ohlcv = pu.get_ohlcv(ticker, interval=interval, count=2)
        trade_volumes[ticker] = get_recent_trade_volume(ticker, ohlcv)

    return [ticker for ticker, _ in sorted(trade_volumes.items(), key=lambda x: x[1], reverse=True)[:top_n]]
