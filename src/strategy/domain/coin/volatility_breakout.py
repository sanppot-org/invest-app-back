import time
import pyupbit as pu
from src.account.domain.account import Account
from src.common.domain.logging_config import logger
from src.common.domain.ticker import Ticker
from src.common.adapter.out.upbit_df_holder import UpbitDfHolder
from src.strategy.domain.coin.coin_strategy import SubStrategy


class VolatilityBreakoutStrategy(SubStrategy):
    def trade(self, account: Account, ticker: str, amount: float, upbit_df_holder: UpbitDfHolder):
        self._buy(account, ticker, amount, upbit_df_holder)
        self._sell(account, ticker)

    def _buy(self, account: Account, ticker: str, amount: float, upbit_df_holder: UpbitDfHolder):
        buy_weight = self._calculate_buy_weight(upbit_df_holder)

        if buy_weight == 0:
            return

        # 현재가 조회
        current_price = float(pu.get_current_price(ticker))

        if not self._should_buy(current_price, upbit_df_holder):
            return

        invest_amount = amount * buy_weight

        logger.debug(f"{ticker} {invest_amount} 만큼 매수")

        time.sleep(0.05)
        account.buy_limit_order(Ticker(ticker), price=current_price, quantity=invest_amount / current_price)

    def _sell(self, account: Account, ticker: str):
        if not self._should_sell():
            return

        time.sleep(0.05)
        account.sell_all(ticker)

    def _should_buy(self, current_price: float, upbit_df_holder: UpbitDfHolder) -> bool:
        """
        매수 조건 : 현재가 > 돌파 기준 가격

        current_price : 현재 가격
        """

        is_price_above_breakout = current_price > self._get_breakout_price(upbit_df_holder)

        logger.debug("======================= should_buy=========================")
        logger.debug(f"current_price (현재 가격): {current_price}")
        logger.debug(f"is_price_above_breakout (현재 가격이 돌파 기준 가격보다 높은지): {is_price_above_breakout}")
        logger.debug("======================= should_buy =========================")

        return self.time_util.is_morning() and is_price_above_breakout

    def _should_sell(self) -> bool:
        return self.time_util.is_afternoon()

    def _get_breakout_price(self, upbit_df_holder: UpbitDfHolder) -> float:
        """
        돌파 기준 가격 설정
        돌파 기준 가격 : 당일 시가(0시) + 전일 오전 레인지 * 20일 노이즈 비율 평균
        """

        today_open = upbit_df_holder.get_yesterday_close()
        yesterday_morning_range = upbit_df_holder.get_yesterday_morning_range()
        recent_20_days_noise_mean = upbit_df_holder.get_recent_20_days_noise_mean()
        breakout_price = float(today_open + yesterday_morning_range * recent_20_days_noise_mean)

        logger.debug("======================= get_breakout_price =========================")
        logger.debug(f"today_open (오늘 0시 시가): {today_open}")
        logger.debug(f"yesterday_morning_range (전일 오전 레인지): {yesterday_morning_range}")
        logger.debug(f"recent_20_days_noise_mean (20일 노이즈 비율 평균): {recent_20_days_noise_mean}")
        logger.debug(f"breakout_price (돌파 기준 가격): {breakout_price}")
        logger.debug("======================= get_breakout_price =========================")

        return breakout_price

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

        return calculated_ratio * upbit_df_holder.calculate_ma_score(upbit_df_holder.get_yesterday_close())
