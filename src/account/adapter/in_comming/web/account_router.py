from fastapi import APIRouter, Depends
from src.account.adapter.out.kis.kis_account_validator import KisAccountValidator
from src.account.application.port.out.account_repository import AccountRepository
from src.account.application.service.account_provider import AccountProvider
from src.common.domain.ticker import Ticker
from src.common.domain.type import Market
from src.account.domain.account import Account
from src.account.adapter.out.kis import token_refresher
from src.account.adapter.in_comming.web.model import AccountCreateReq
from dependency_injector.wiring import inject, Provide

from src.containers import Container


router = APIRouter(prefix="/accounts", tags=["account"])
kis_account_validator = KisAccountValidator()


@router.post("/", summary="계좌 생성")
@inject
async def save(req: AccountCreateReq, account_repo: AccountRepository = Depends(Provide[Container.account_repository])):
    account_info = req.to_domain()
    kis_account_validator.validate(account_info)
    return account_repo.save(account_info)


@router.put("/{id}", summary="계좌 수정")
@inject
async def update(id: int, req: AccountCreateReq, account_repo: AccountRepository = Depends(Provide[Container.account_repository])):
    account_info = req.to_domain()
    kis_account_validator.validate(account_info)
    return account_repo.update(id, account_info)


@router.get("/", summary="계좌 목록 조회")
@inject
async def find_all(account_repo: AccountRepository = Depends(Provide[Container.account_repository])):
    return account_repo.find_all()


@router.get("/{id}", summary="계좌 상세 조회")
@inject
async def find_by_id(id: int, account_repo: AccountRepository = Depends(Provide[Container.account_repository])):
    return account_repo.find_by_id(id)


@router.delete("/{id}", summary="계좌 삭제")
@inject
async def delete(id: int, account_repo: AccountRepository = Depends(Provide[Container.account_repository])):
    return account_repo.delete_by_id(id)


@router.get("/{id}/balance", summary="잔고 조회")
@inject
async def get_balance(id: int, market: Market = Market.KR, account_provider: AccountProvider = Depends(Provide[Container.account_provider])):
    account: Account = account_provider.get_account(id)
    return account.get_balance(market)


@router.post("/{id}/buy", summary="시장가 매수")
@inject
async def buy(id: int, ticker: Ticker, quantity: int, account_provider: AccountProvider = Depends(Provide[Container.account_provider])):
    account: Account = account_provider.get_account(id)
    return account.buy_market_order(ticker, quantity)


@router.get("/{id}/holdings", summary="보유 종목 조회")
@inject
async def get_holdings(id: int, market: Market = Market.KR, account_provider: AccountProvider = Depends(Provide[Container.account_provider])):
    account: Account = account_provider.get_account(id)
    return account.get_holdings(market)


@router.post("/refresh-kis-token", summary="한투 토큰 갱신 (전체)")
@inject
async def refresh_kis_token_all(account_repo: AccountRepository = Depends(Provide[Container.account_repository])):
    return token_refresher.refresh_kis_token(account_repo)
