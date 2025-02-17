from src.strategy.domain.coin.am_pm import AmPmStrategy
from src.strategy.domain.coin.coin_strategy import CoinStrategy
from src.strategy.domain.coin.volatility_breakout import VolatilityBreakoutStrategy
from src.strategy.domain.static_asset import StaticAssetStrategy
from src.strategy.domain.strategy_info import StrategyInfo
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity
from src.strategy.domain.strategy_type import StrategyType
from strategy_new.vol_strategy import VolStrategy


class StrategyMapper:
    def to_entity(self, model: StrategyInfo) -> StrategyEntity:
        additional_data = {}

        if isinstance(model, StaticAssetStrategy):
            additional_data = {"market": model.market, "stocks": model.stocks, "interval": model.interval}
        elif isinstance(model, CoinStrategy):
            additional_data = {"timezone": model.timezone, "coin_count": model.coin_count, "coin_list": model.coin_list}
        elif isinstance(model, VolatilityBreakoutStrategy):
            additional_data = {"target_volatility": model.target_volatility}
        elif isinstance(model, AmPmStrategy):
            additional_data = {"timezone": model.timezone}

        return StrategyEntity(
            id=model.id,
            name=model.name,
            invest_rate=model.invest_rate,
            account_id=model.account_id,
            strategy_type=model.strategy_type,
            last_run=model.last_run,
            is_active=model.is_active,
            additional_data=additional_data,
        )

    def to_model(self, entity: StrategyEntity) -> StrategyInfo:

        if entity.strategy_type == StrategyType.STATIC_ASSET:
            return StaticAssetStrategy(
                id=entity.id,
                name=entity.name,
                invest_rate=entity.invest_rate,
                account_id=entity.account_id,
                strategy_type=entity.strategy_type,
                last_run=entity.last_run,
                is_active=entity.is_active,
                market=entity.additional_data["market"],
                stocks=entity.additional_data["stocks"],
                interval=entity.additional_data["interval"],
            )

        elif entity.strategy_type == StrategyType.COIN:
            return CoinStrategy(
                id=entity.id,
                name=entity.name,
                invest_rate=entity.invest_rate,
                account_id=entity.account_id,
                strategy_type=entity.strategy_type,
                last_run=entity.last_run,
                is_active=entity.is_active,
                coin_list=entity.additional_data["coin_list"],
                timezone=entity.additional_data["timezone"],
                coin_count=entity.additional_data["coin_count"],
            )

        elif entity.strategy_type == StrategyType.VOLATILITY_BREAKOUT:
            return VolStrategy()

        raise ValueError(f"Invalid strategy type: {entity.strategy_type}")
