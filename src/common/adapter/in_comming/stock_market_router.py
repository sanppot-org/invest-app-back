from fastapi import APIRouter, Query
from src.common.adapter.out.stock_market_client import StockMarketClient
from src.common.domain.ticker import Ticker
from src.common.domain.type import Market


router = APIRouter(prefix="/stock-market", tags=["stock-market"])

stock_market_client = StockMarketClient()


@router.get("/is-market-open", summary="시장 열려있는지 확인")
def is_market_open(market: Market = Query(default=Market.KR)):
    return stock_market_client.is_market_open(market)


@router.get("/current-price", summary="주식 현재가 조회", description="""한국 주식은 .KS를 붙여야한다.""")
def get_current_price(ticker: str):
    return stock_market_client.get_current_price(Ticker(ticker.upper()))
