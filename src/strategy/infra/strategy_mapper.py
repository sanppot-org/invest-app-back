from src.common.infra.entity_mapper import EntityMapper
from src.strategy.infra.strategy_entity import StrategyEntity
from src.strategy.strategy import Strategy


class StrategyMapper(EntityMapper[Strategy, StrategyEntity]):
    def to_entity(self, domain: Strategy) -> StrategyEntity:
        return StrategyEntity(
            id=domain.id,
            name=domain.name,
            account_id=domain.account_id,
            last_executed_at=domain.last_executed_at,
            tz=domain.tz,
            type=domain.type,
            target_volatility=domain.target_volatility,
            is_active=domain.is_active,
            tickers=domain.tickers,
        )

    def to_domain(self, entity: StrategyEntity) -> Strategy:
        return Strategy(
            id=entity.id,
            name=entity.name,
            account_id=entity.account_id,
            last_executed_at=entity.last_executed_at,
            tz=entity.tz,
            type=entity.type,
            target_volatility=entity.target_volatility,
            is_active=entity.is_active,
            tickers=entity.tickers,
        )
