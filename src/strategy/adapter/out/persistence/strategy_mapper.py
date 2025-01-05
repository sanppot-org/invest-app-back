from src.strategy.domain.strategy import Strategy
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity


class StrategyMapper:
    def to_entity(self, model: Strategy) -> StrategyEntity:
        return StrategyEntity(
            id=model.id,
            name=model.name,
            invest_rate=model.invest_rate,
            market=model.market,
            stocks=model.stocks,
            interval=model.interval,
            last_run=model.last_run,
            account_id=model.account_id,
            is_active=model.is_active,
        )

    def to_model(self, entity: StrategyEntity) -> Strategy:
        return Strategy(
            id=entity.id,
            name=entity.name,
            invest_rate=entity.invest_rate,
            market=entity.market,
            stocks=entity.stocks,
            interval=entity.interval,
            last_run=entity.last_run,
            account_id=entity.account_id,
            is_active=entity.is_active,
        )
