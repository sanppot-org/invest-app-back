from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from src.account.account import Account
from src.account.account_service import AccountService
from src.containers import Container

router = APIRouter(prefix="/accounts", tags=["account"])


@router.get("/{id}/balance", summary="잔고 조회")
@inject
async def get_balance(id: int, account_service: AccountService = Depends(Provide[Container.account_service])):
    account: Account = account_service.find_by_id(id)
    account_operator = account_service.get_operator(account)
    return account_operator.get_balance()


@router.get("/{id}/holdings", summary="보유 종목 조회")
@inject
async def get_holdings(id: int, account_service: AccountService = Depends(Provide[Container.account_service])):
    account: Account = account_service.find_by_id(id)
    account_operator = account_service.get_operator(account)
    return account_operator.get_holdings()
