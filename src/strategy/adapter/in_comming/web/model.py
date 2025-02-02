from typing import Callable, Dict, Optional, Union
from pydantic import BaseModel, Field, field_validator

from src.common.domain.type import Market
from src.strategy.domain.coin.coin_strategy import CoinStrategy
from src.strategy.domain.interval import Interval
from src.strategy.domain.static_asset import StaticAssetStrategy
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy import Strategy
from src.strategy.domain.strategy_type import StrategyType


# 각 전략별 전용 DTO
class StaticAssetStrategyDTO(BaseModel):
    market: Market
    stocks: Dict[str, StockInfo]
    interval: Interval


class CoinStrategyDTO(BaseModel):
    timezone: str
    coin_count: int


class StrategyCreateReq(BaseModel):
    name: str
    invest_rate: float = Field(..., ge=0, le=1)
    account_id: int
    is_active: Optional[bool] = False
    strategy_type: StrategyType
    data: Union[StaticAssetStrategyDTO, CoinStrategyDTO]

    # Pydantic validator를 사용하여 전략 유형에 맞는 DTO인지 검증
    @field_validator("data")
    def validate_strategy_data(cls, v, values):
        strategy_type = values.data.get("strategy_type")
        if strategy_type == StrategyType.STATIC_ASSET and not isinstance(v, StaticAssetStrategyDTO):
            raise ValueError("Invalid data type for STATIC_ASSET strategy")
        if strategy_type == StrategyType.COIN and not isinstance(v, CoinStrategyDTO):
            raise ValueError("Invalid data type for COIN strategy")
        return v

    def to_domain(self) -> Strategy:
        strategy_factories: Dict[StrategyType, Callable[[], Strategy]] = {
            StrategyType.STATIC_ASSET: self._create_static_asset_strategy,
            StrategyType.COIN: self._create_coin_strategy,
        }

        factory = strategy_factories.get(self.strategy_type)

        if not factory:
            raise ValueError(f"Unsupported strategy type: {self.strategy_type}")

        return factory()

    def _create_static_asset_strategy(self) -> StaticAssetStrategy:
        return StaticAssetStrategy(
            id=None,
            name=self.name,
            invest_rate=self.invest_rate,
            account_id=self.account_id,
            strategy_type=self.strategy_type,
            last_run=None,
            is_active=self.is_active or False,
            market=self.data.market,
            stocks=self.data.stocks,
            interval=self.data.interval,
        )

    def _create_coin_strategy(self) -> CoinStrategy:
        return CoinStrategy(
            id=None,
            name=self.name,
            invest_rate=self.invest_rate,
            account_id=self.account_id,
            strategy_type=self.strategy_type,
            last_run=None,
            is_active=self.is_active or False,
            timezone=self.data.timezone,
            coin_count=self.data.coin_count,
        )
