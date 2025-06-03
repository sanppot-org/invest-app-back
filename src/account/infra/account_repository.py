from src.infrastructure.exchange.exchange_client_factory import ExchangeClientFactory
from src.account.account_operator import AccountOperator
from src.account.account import Account
from src.account.infra.account_mapper import AccountMapper
from src.db.generic_repository import GenericRepository
from src.db.sqlalchemy_repository import SqlalchemyRepository
from src.db.database_session_manager import DBSessionManager
from src.account.infra.account_entity import AccountEntity


class AccountRepository(GenericRepository[Account, AccountEntity]):
    def __init__(
        self,
        account_mapper: AccountMapper,
        account_repository: SqlalchemyRepository[AccountEntity],
        session_manager: DBSessionManager,
        exchange_client_factory: ExchangeClientFactory,
    ):
        super().__init__(account_mapper, account_repository, session_manager)
        self.exchange_client_factory = exchange_client_factory

    def get_operator(self, account_id: int) -> AccountOperator:
        account: Account = self.find_by_id(account_id)
        exchange_client = self.exchange_client_factory.create(account.broker_type, account.app_key, account.secret_key)
        return AccountOperator(account, exchange_client)
