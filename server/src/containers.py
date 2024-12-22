from dependency_injector import containers, providers
from src.account.application.account_service import AccountService
from src.account.application.port.out.account_repository import AccountRepository
from src.account.adapter.out.stock.stock_market import StockMarketClientImpl
from src.common.persistence import engine
from src.account.adapter.out.persistence.account_mapper import AccountMapper
from src.account.adapter.out.persistence.sqlalchemy_account_repository import SqlAlchemyAccountRepository
from src.domain.strategy.strategy_service import StrategyService
from src.infra.strategy.persistance.strategy_mapper import StrategyMapper
from src.infra.strategy.persistance.strategy_repo import SqlAlchemyStrategyRepository


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
    strategy_mapper = providers.Singleton(StrategyMapper)
    strategy_repository = providers.Singleton(
        SqlAlchemyStrategyRepository,
        session=session,
        mapper=strategy_mapper,
    )

    account_mapper = providers.Singleton(AccountMapper)
    account_repository = providers.Singleton(
        SqlAlchemyAccountRepository,
        session=session,
        mapper=account_mapper,
    )

    account_service = providers.Singleton(AccountService, account_repository=account_repository)

    account_provider = providers.Singleton(RealAccountProvider, account_repository=account_repository)

    stock_market_client = providers.Singleton(StockMarketClientImpl)
    time_holder = providers.Singleton(TimeHolderImpl)

    strategy_service = providers.Singleton(
        StrategyService,
        stock_market_client=stock_market_client,
        time_holder=time_holder,
        account_provider=account_provider,
        strategy_repo=strategy_repository,
    )
