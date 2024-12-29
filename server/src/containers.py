from dependency_injector import containers, providers
from src.account.application.service.account_provider import RealAccountProvider
from src.common.adapter.out.persistence import engine
from src.common.domain.time_holder import TimeHolderImpl
from src.common.adapter.out.stock_market_client import StockMarketClient
from src.account.adapter.out.persistence.account_repo import SqlAlchemyAccountRepository
from src.strategy.adapter.out.persistence.strategy_repo import SqlAlchemyStrategyRepository
from src.strategy.application.service.strategy_service import StrategyService


class Container(containers.DeclarativeContainer):
    _instance = None

    def __init__(self):
        self.init_resources()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    config = providers.Configuration()

    session = providers.Singleton(engine.get_session)

    strategy_repository = providers.Singleton(
        SqlAlchemyStrategyRepository,
        session=session,
    )

    account_repository = providers.Singleton(
        SqlAlchemyAccountRepository,
        session=session,
    )

    account_provider = providers.Singleton(RealAccountProvider, account_repository=account_repository)

    stock_market_query_port = providers.Singleton(StockMarketClient)
    time_holder = providers.Singleton(TimeHolderImpl)

    strategy_service = providers.Singleton(
        StrategyService,
        stock_market_query_port=stock_market_query_port,
        time_holder=time_holder,
        account_provider=account_provider,
        strategy_repo=strategy_repository,
    )
