from fastapi import APIRouter
from src.account.adapter.out.kis.kis_account_validator import KisAccountValidator
from src.common.domain.ticker import Ticker
from src.common.domain.type import Market
from src.containers import Container
from src.account.domain.account import Account
from src.account.adapter.out.kis import token_refresher
from src.account.adapter.in_comming.web.model import AccountCreateReq


router = APIRouter(prefix="/accounts", tags=["account"])


container = Container.get_instance()
account_repo = container.account_repository()
account_provider = container.account_provider()
kis_account_validator = KisAccountValidator()


@router.post("/", summary="계좌 생성")
def save(req: AccountCreateReq):
    account_info = req.to_domain()
    kis_account_validator.validate(account_info)
    return account_repo.save(account_info)


@router.put("/{id}", summary="계좌 수정")
def update(id: int, req: AccountCreateReq):
    account_info = req.to_domain()
    kis_account_validator.validate(account_info)
    return account_repo.update(id, account_info)


@router.get("/", summary="계좌 목록 조회")
def find_all():
    return account_repo.find_all()


@router.get("/{id}", summary="계좌 상세 조회")
def find_by_id(id: int):
    return account_repo.find_by_id(id)


@router.delete("/{id}", summary="계좌 삭제")
def delete(id: int):
    return account_repo.delete_by_id(id)


@router.get("/{id}/balance", summary="잔고 조회")
def get_balance(id: int, market: Market = Market.KR):
    account: Account = account_provider.get_account(id)
    return account.get_balance(market)


@router.post("/{id}/buy", summary="시장가 매수")
def buy(id: int, ticker: Ticker, quantity: int):
    account: Account = account_provider.get_account(id)
    return account.buy_market_order(ticker, quantity)


@router.get("/{id}/holdings", summary="보유 종목 조회")
def get_holdings(id: int, market: Market = Market.KR):
    account: Account = account_provider.get_account(id)
    return account.get_holdings(market)


@router.post("/refresh-kis-token", summary="한투 토큰 갱신 (전체)")
def refresh_kis_token_all():
    return token_refresher.refresh_kis_token()
