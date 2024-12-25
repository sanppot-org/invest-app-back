import exchange_calendars as market_calendar
import pyupbit
import yfinance as yf

from src.common.application.port.out.stock_market_port import StockMarketQueryPort
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import Market


class StockMarketClient(StockMarketQueryPort):
    def is_market_open(self, market: Market):
        if market.is_market_open_time() and self._is_market_open_date(market):
            return

        raise InvestAppException(ExeptionType.MARKET_NOT_OPEN, market.name, market.get_now().replace(microsecond=0))

    def _is_market_open_date(self, market: Market):
        calendar = market_calendar.get_calendar("XNYS")

        if market.is_kr():
            calendar = market_calendar.get_calendar("XKRX")

        return calendar.is_session(market.get_now().strftime("%Y-%m-%d"))

    def get_current_price(self, ticker: str) -> float:
        if ticker.upper().startswith("KRW-"):
            return float(pyupbit.get_current_price(ticker))

        return float(yf.Ticker(ticker).fast_info.last_price)
