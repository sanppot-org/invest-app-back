from fastapi import APIRouter
from src.account.adapter.in_comming.web.model import AccountCreateReq
from src.containers import Container
from src.account.domain.interface import Account
from src.account.adapter.out.kis import token_refresher


router = APIRouter(prefix="/accounts", tags=["account"])


container = Container.get_instance()
account_service = container.account_service()


@router.post("/", summary="계좌 생성")
def save(req: AccountCreateReq):
    return account_service.save(req.to_domain())


@router.put("/{id}", summary="계좌 수정")
def update(id: int, req: AccountCreateReq):
    return account_service.update(id, req.to_domain())


@router.get("/", summary="계좌 목록 조회")
def find_all():
    return account_service.find_all()


@router.get("/{id}", summary="계좌 상세 조회")
def find_by_id(id: int):
    return account_service.find_by_id(id)


@router.delete("/{id}", summary="계좌 삭제")
def delete(id: int):
    return account_service.delete_by_id(id)


@router.get("/{id}/balance", summary="잔고 조회")
def get_balance(id: int):
    return account_service.get_balance(id)


@router.get("/{id}/holdings", summary="보유 종목 조회")
def get_holdings(id: int):
    return account_service.get_holdings(id)


# @router.get("/{id}/current-price", summary="현재 가격 조회")
# def get_current_price(id: int, ticker: str):
#     return account_service.get_current_price(id, ticker)


@router.post("/refresh-kis-token", summary="한투 토큰 갱신 (전체)")
def refresh_kis_token_all():
    return token_refresher.refresh_kis_token()
