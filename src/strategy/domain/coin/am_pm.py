import time
from src.account.domain.account import Account
from src.common.adapter.out.upbit_df_holder import UpbitDfHolder
from src.common.domain.ticker import Ticker
from src.common.domain.logging_config import logger
from src.strategy.domain.coin.sub_strategy import SubStrategy


class AmPmStrategy(SubStrategy):
    def trade(self, account: Account, ticker: str, amount: float, upbit_df_holder: UpbitDfHolder):
        logger.debug(f"=============== {ticker} 오전,오후 전략 시작 =================")
        logger.debug(f"할당 금액 : {amount}")

        self._buy(account, ticker, amount, upbit_df_holder)
        self._sell(account, ticker)

        logger.debug(f"=============== {ticker} 오전,오후 전략 완료 =================")

    def _buy(self, account: Account, ticker: str, amount: float, upbit_df_holder: UpbitDfHolder):
        if not self._should_buy(upbit_df_holder):
            return

        logger.debug(f"{ticker} 매수")

        buy_weight = self._calculate_buy_weight(upbit_df_holder)
        invest_amount = amount * buy_weight
        time.sleep(0.03)
        account.buy_market_order(Ticker(ticker), invest_amount)

    def _sell(self, account: Account, ticker: str):
        if not self._should_sell():
            return

        time.sleep(0.03)
        account.sell_all(ticker)

    def _should_buy(self, upbit_df_holder: UpbitDfHolder) -> bool:
        """
        매수 조건 : 오전 && 전일 오후 수익률 > 0 and 전일 오후 거래량 > 전일 오전 거래량
        """

        return (
            self.time_util.is_morning()
            and self._is_yesterday_afternoon_return_positive(upbit_df_holder)
            and self._is_yesterday_afternoon_volume_higher_than_morning(upbit_df_holder)
        )

    def _should_sell(self) -> bool:
        """
        매도 조건 : 오후
        """
        return self.time_util.is_afternoon()

    def _calculate_buy_weight(self, upbit_df_holder: UpbitDfHolder) -> float:
        """
        매수 비중 계산
        """

        yesterday_morning_volatility = upbit_df_holder.get_yesterday_morning_volatility()
        calculated_ratio = min(1, self.target_volatility / yesterday_morning_volatility)

        logger.debug("======================= calculate_buy_weight =========================")
        logger.debug(f"target_volatility (타겟 변동성): {self.target_volatility}")
        logger.debug(f"yesterday_morning_volatility (전일 오전 변동성): {yesterday_morning_volatility}")
        logger.debug(f"calculate_buy_weight (매수 비중): {calculated_ratio}")
        logger.debug("======================= calculate_buy_weight =========================")

        return calculated_ratio

    def _is_yesterday_afternoon_return_positive(self, upbit_df_holder: UpbitDfHolder) -> bool:
        """
        어제 오후 수익률이 양수인지 확인

        df_afternoon_grouped : 최근 20일의 오후 데이터
        """
        df_yesterday_afternoon = upbit_df_holder.df_yesterday_afternoon
        yesterday_afternoon_close = df_yesterday_afternoon["close"].values[0]
        yesterday_afternoon_open = df_yesterday_afternoon["open"].values[0]

        yesterday_afternoon_return = (yesterday_afternoon_close - yesterday_afternoon_open) / yesterday_afternoon_open

        is_positive_return = bool(yesterday_afternoon_return > 0)

        logger.debug("======================= is_yesterday_afternoon_return_positive =========================")
        logger.debug(f"yesterday_afternoon_close (어제 오후 종가): {yesterday_afternoon_close}")
        logger.debug(f"yesterday_afternoon_open (어제 오후 시가): {yesterday_afternoon_open}")
        logger.debug(f"yesterday_afternoon_return (어제 오후 수익률): {yesterday_afternoon_return}")
        logger.debug(f"is_positive_return (어제 오후 수익률이 양수인지): {is_positive_return}")
        logger.debug("======================= is_yesterday_afternoon_return_positive =========================")

        return is_positive_return

    def _is_yesterday_afternoon_volume_higher_than_morning(self, upbit_df_holder: UpbitDfHolder) -> bool:
        """
        어제 오후 거래량이 오전 거래량보다 높은지 확인
        """

        yesterday_morning_volume = upbit_df_holder.df_yesterday_morning["volume"].values[0]
        yesterday_afternoon_volume = upbit_df_holder.df_yesterday_afternoon["volume"].values[0]

        logger.debug("======================= is_yesterday_afternoon_volume_higher_than_morning =========================")
        logger.debug(f"yesterday_morning_volume (어제 오전 거래량): {yesterday_morning_volume}")
        logger.debug(f"yesterday_afternoon_volume (어제 오후 거래량): {yesterday_afternoon_volume}")
        logger.debug("======================= is_yesterday_afternoon_volume_higher_than_morning =========================")

        return bool(yesterday_morning_volume < yesterday_afternoon_volume)
