from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.account.infra.account_entity import AccountEntity
from src.account.infra.account_mapper import AccountMapper
from src.account.infra.account_repository import AccountRepository
from src.common.infra.database_session_manager import DBSessionManager
from src.common.infra.sqlalchemy_repository import SqlalchemyRepository
from src.infrastructure.crypto_market_data_client import CryptoMarketDataClient
from src.infrastructure.exchange.exchange_client_factory import ExchangeClientFactory
from src.strategy.ampm_strategy_service import AmpmStrategyService
from src.strategy.infra.strategy_entity import StrategyEntity
from src.strategy.infra.strategy_mapper import StrategyMapper
from src.strategy.infra.strategy_repository import StrategyRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Resource(create_engine, url=config.DB_URL, echo=True)
    session_factory = providers.Factory(sessionmaker, bind=engine)
    db_session_manager = providers.Singleton(DBSessionManager, session_factory)
    exchange_client_factory = providers.Singleton(ExchangeClientFactory)
    crypto_market_data_client_factory = providers.Singleton(CryptoMarketDataClient)
    account_sqlalchemy_repository = providers.Singleton(SqlalchemyRepository, entity_type=AccountEntity)
    strategy_sqlalchemy_repository = providers.Singleton(SqlalchemyRepository, entity_type=StrategyEntity)
    account_mapper = providers.Singleton(AccountMapper)
    account_repository = providers.Singleton(
        AccountRepository,
        mapper=account_mapper,
        repository=account_sqlalchemy_repository,
        session_manager=db_session_manager,
        exchange_client_factory=exchange_client_factory,
    )
    strategy_mapper = providers.Singleton(StrategyMapper)
    strategy_repository = providers.Singleton(
        StrategyRepository,
        mapper=strategy_mapper,
        repository=strategy_sqlalchemy_repository,
        session_manager=db_session_manager,
    )
    ampm_strategy_service = providers.Singleton(
        AmpmStrategyService,
        crypto_market_data_client=crypto_market_data_client_factory,
        account_repository=account_repository,
        strategy_repository=strategy_repository,
    )
