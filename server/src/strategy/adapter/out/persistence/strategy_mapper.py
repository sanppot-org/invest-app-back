from src.strategy.domain.strategy import StrategyDomainModel
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity
from src.strategy.domain.strategy_upsert_command import StrategyCreateCommand


class StrategyMapper:
    def to_entity(self, command: StrategyCreateCommand) -> StrategyEntity:
        return StrategyEntity(
            name=command.name,
            invest_rate=command.invest_rate,
            market=command.market,
            stocks=command.stocks,
            interval=command.interval,
            account_id=command.account_id,
            is_active=command.is_active,
        )

    def to_model(self, entity: StrategyEntity) -> StrategyDomainModel:
        return StrategyDomainModel(
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
