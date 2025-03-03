from fastapi import APIRouter, Depends
from src.containers import Container
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.application.service.strategy_service import StrategyService
from src.strategy.adapter.in_comming.web.model import StrategyCreateReq
from src.strategy.domain.strategy import Strategy
from dependency_injector.wiring import inject, Provide


router = APIRouter(prefix="/strategies", tags=["strategy"])


@router.get("/", summary="전략 목록 조회")
@inject
async def find_all(strategy_repo: StrategyRepository = Depends(Provide[Container.strategy_repository])):
    return strategy_repo.find_all()


@router.post("/", summary="전략 생성")
@inject
async def save(req: StrategyCreateReq, strategy_repo: StrategyRepository = Depends(Provide[Container.strategy_repository])):
    model: Strategy = req.to_domain()
    model.validate()
    return strategy_repo.save(model)


@router.put("/{id}", summary="전략 수정")
@inject
async def update(id: int, req: StrategyCreateReq, strategy_repo: StrategyRepository = Depends(Provide[Container.strategy_repository])):
    model = req.to_domain()
    model.validate()
    return strategy_repo.update(id, model)


@router.get("/{id}", summary="전략 상세 조회")
@inject
async def get(id: int, strategy_repo: StrategyRepository = Depends(Provide[Container.strategy_repository])):
    return strategy_repo.find_by_id(id)


@router.delete("/{id}", summary="전략 삭제")
@inject
async def delete(id: int, strategy_repo: StrategyRepository = Depends(Provide[Container.strategy_repository])):
    return strategy_repo.delete_by_id(id)


@router.post("/{id}/trade", summary="전략 실행")
@inject
async def trade(id: int, strategy_service: StrategyService = Depends(Provide[Container.strategy_service])):
    strategy_service.trade(id)
