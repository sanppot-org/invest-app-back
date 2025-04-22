from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.exchange_client_factory import ExchangeClientFactory
from src.account.account_mapper import AccountMapper
from src.account.account_service import AccountService
from .config import DB_URL
from src.db.database_session_manager import DBSessionManager
from src.db.account_entity import AccountEntity
from src.db.sqlalchemy_repository import SqlalchemyRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton(create_engine, url=DB_URL, echo=True)
    session_factory = providers.Factory(sessionmaker, bind=engine)
    db_session_manager = providers.Singleton(DBSessionManager, session_factory)
    exchange_client_factory = providers.Singleton(ExchangeClientFactory)
    account_sqlalchemy_repository = providers.Singleton(SqlalchemyRepository, entity_type=AccountEntity)
    account_mapper = providers.Singleton(AccountMapper)
    account_service = providers.Singleton(
        AccountService,
        account_mapper=account_mapper,
        account_repository=account_sqlalchemy_repository,
        session_manager=db_session_manager,
        exchange_client_factory=exchange_client_factory,
    )
