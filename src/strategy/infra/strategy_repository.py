from src.common.infra.database_session_manager import DBSessionManager
from src.common.infra.generic_repository import GenericRepository
from src.common.infra.sqlalchemy_repository import SqlalchemyRepository
from src.strategy.infra.strategy_entity import StrategyEntity
from src.strategy.infra.strategy_mapper import StrategyMapper
from src.strategy.strategy import Strategy


class StrategyRepository(GenericRepository[Strategy, StrategyEntity]):
    def __init__(
            self,
            mapper: StrategyMapper,
            repository: SqlalchemyRepository[StrategyEntity],
            session_manager: DBSessionManager,
    ):
        super().__init__(mapper, repository, session_manager)
