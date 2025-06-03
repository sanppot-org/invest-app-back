from pandas import DataFrame

from src.account.account_operator import AccountOperator
from src.account.infra.account_repository import AccountRepository
from src.common.logging_config import logger
from src.infrastructure.crypto_market_data_client import CryptoMarketDataClient
from src.infrastructure.exchange import df_column
from src.infrastructure.time_holder import TimeHolder
from src.infrastructure.timezone import TimeZone
from src.strategy.infra.strategy_repository import StrategyRepository
from src.strategy.strategy import Strategy


class AmpmStrategyService:
    def __init__(
            self,
            crypto_market_data_client: CryptoMarketDataClient,
            account_repository: AccountRepository,
            strategy_repository: StrategyRepository,
    ):
        self.crypto_market_data_client = crypto_market_data_client
        self.account_repository = account_repository
        self.strategy_repository = strategy_repository

    def execute(self, strategy: Strategy):
        if strategy.is_afternoon():
            self._process_afternoon(strategy)
            return

        self._process_morning(strategy)

    def _process_afternoon(self, strategy: Strategy):
        """
        오후 작업
        """
        if strategy.is_last_execution_time_this_afternoon():
            return

        account_operator: AccountOperator = self.account_repository.get_operator(strategy.account_id)
        account_operator.sell_all()
        self._update(strategy)

    def _process_morning(self, strategy: Strategy):
        """
        오전 작업
        """
        if strategy.is_last_execution_time_this_morning():
            return

        # top_n_volume_tickers: list[str] = self.crypto_market_data_client.get_top_n_volume_tickers()  # TODO: 고도화하기
        account_operator: AccountOperator = self.account_repository.get_operator(strategy.account_id)

        # for ticker in top_n_volume_tickers: # TODO: 고도화하기
        for ticker in strategy.tickers:
            self._buy(ticker, account_operator, strategy.target_volatility, strategy.tz)
        self._update(strategy)

    def _buy(self, ticker: str, account_operator: AccountOperator, target_volatility: float, tz: TimeZone):
        if not (self._is_last_day_afternoon_profitable(ticker, tz) and self._is_last_day_afternoon_volume_positive(ticker, tz)):
            logger.debug(f"매수 조건 불충족 - ticker: {ticker}")
            return

        buy_weight: float = self._get_buy_weight(ticker, target_volatility, tz)
        account_operator.buy_market_order(ticker=ticker, weight=buy_weight)

    def _is_last_day_afternoon_profitable(self, ticker: str, tz: TimeZone) -> bool:
        """
        전일 오후 수익률이 양수인지 확인
        """
        last_day_ohlcv: DataFrame = self.crypto_market_data_client.get_last_day_hourly_ohlcv(ticker=ticker, tz=tz)
        pm_open: float = last_day_ohlcv[last_day_ohlcv[df_column.IS_MORNING] == False].iloc[-1][df_column.OPEN]
        pm_close: float = last_day_ohlcv[last_day_ohlcv[df_column.IS_MORNING] == False].iloc[0][df_column.CLOSE]
        is_last_day_afternoon_profitable = pm_open < pm_close
        logger.debug(f"[오전오후] ticker: {ticker} 전일 오후 수익률 > 0 : {is_last_day_afternoon_profitable} 시가: {pm_open}, 종가: {pm_close}")
        return is_last_day_afternoon_profitable

    def _is_last_day_afternoon_volume_positive(self, ticker: str, tz: TimeZone) -> bool:
        """
        전일 오후 거래량 > 전일 오전 거래량
        """
        last_day_ohlcv: DataFrame = self.crypto_market_data_client.get_last_day_hourly_ohlcv(ticker=ticker, tz=tz)
        am_volume = last_day_ohlcv[last_day_ohlcv[df_column.IS_MORNING] == True][df_column.VOLUME].sum()
        pm_volume = last_day_ohlcv[last_day_ohlcv[df_column.IS_MORNING] == False][df_column.VOLUME].sum()
        is_last_day_afternoon_volume_positive = am_volume < pm_volume
        logger.debug(f"[오전오후] ticker: {ticker} 전일 오후 거래량 > 오전 거래량 : {is_last_day_afternoon_volume_positive} 오전 거래량: {am_volume}, 오후 거래량: {pm_volume}")
        return is_last_day_afternoon_volume_positive

    def _get_buy_weight(self, ticker: str, target_volatility: float, tz: TimeZone) -> float:
        """
        매수 비중 확인

        매수 비중: 타겟 변동성 / 전일 오전 변동성
        전일 오전 변동성: 오전 레인지(오전 고가 - 오전 저가)/오전 시가
        """

        last_day_ohlcv: DataFrame = self.crypto_market_data_client.get_last_day_hourly_ohlcv(ticker=ticker, tz=tz)
        # 오전 분리
        morning_ohlcv: DataFrame = last_day_ohlcv[last_day_ohlcv[df_column.IS_MORNING] == True]
        # 오전 변동성
        high = morning_ohlcv[df_column.HIGH].max()
        low = morning_ohlcv[df_column.LOW].min()
        open = morning_ohlcv[df_column.OPEN][0]
        morning_volatility: float = (high - low) / open

        return target_volatility / morning_volatility

    def _update(self, strategy):
        strategy.update_last_executed_at()
        self.strategy_repository.update(strategy.id, strategy)
