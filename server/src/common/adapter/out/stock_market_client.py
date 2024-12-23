from datetime import datetime
import exchange_calendars as market_calendar

from src.common.application.port.out.stock_market_client import StockMarketClient
from src.domain.common.type import Market


class StockMarketClientImpl(StockMarketClient):
    def is_market_open(self, market: Market):
        if market.is_kr():
            return market_calendar.get_calendar("XKRX").is_session(datetime.now().date())
        return market_calendar.get_calendar("XNYS").is_session(datetime.now().date())
