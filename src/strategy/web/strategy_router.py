from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.config.containers import Container
from src.strategy.ampm_strategy_service import AmpmStrategyService
from src.strategy.infra.strategy_repository import StrategyRepository
from src.strategy.strategy import Strategy

router = APIRouter(prefix="/strategies", tags=["strategy"])


@router.get("/execute/{id}", summary="전략 실행")
@inject
async def execute(id: int,
                  strategy_repository: StrategyRepository = Depends(Provide[Container.strategy_repository]),
                  ampm_strategy_service: AmpmStrategyService = Depends(Provide[Container.ampm_strategy_service]),
                  ):
    strategy: Strategy = strategy_repository.find_by_id(id)

    if strategy.type.is_ampm():
        ampm_strategy_service.execute(strategy)
