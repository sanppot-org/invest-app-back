from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.account.infra.account_repository import AccountRepository
from src.config.containers import Container

router = APIRouter(prefix="/accounts", tags=["account"])


@router.get("/{id}/balance", summary="잔고 조회")
@inject
async def get_balance(id: int, account_repository: AccountRepository = Depends(Provide[Container.account_repository])):
    account_operator = account_repository.get_operator(id)
    return account_operator.get_balance()


@router.get("/{id}/holdings", summary="보유 종목 조회")
@inject
async def get_holdings(id: int, account_repository: AccountRepository = Depends(Provide[Container.account_repository])):
    account_operator = account_repository.get_operator(id)
    return account_operator.get_holdings()
