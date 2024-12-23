from datetime import datetime
import exchange_calendars as market_calendar

from src.common.application.port.out.stock_market_port import StockMarketQueryPort
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import Market


class StockMarketClient(StockMarketQueryPort):
    def is_market_open(self, market: Market):
        now = datetime.now()
        if self._is_open_time(market, now) and self._is_market_open(market, now):
            return

        raise InvestAppException(ExeptionType.MARKET_NOT_OPEN, now)

    def _is_open_time(self, market: Market, now: datetime):
        if market.is_kr():
            # 한국 주식 시간 - 9:00 ~ 15:25
            return now.hour >= 9 and now.hour <= 15 and now.minute <= 25
        # 미국 주식 시간 - 23:30 ~ 4:55
        return (now.hour >= 23 and now.minute >= 30) or (now.hour <= 4 and now.minute <= 55)

    def _is_market_open(self, market: Market, now: datetime):
        if market.is_kr():
            return market_calendar.get_calendar("XKRX").is_session(now)
        return market_calendar.get_calendar("XNYS").is_session(now)
