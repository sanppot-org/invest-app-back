from src.account.adapter.out.persistence.account_repo import SqlAlchemyAccountRepository
from src.common.adapter.out.persistence.transactional import transactional
from src.containers import Container
from src.common.domain.type import BrokerType
from src.account.adapter.out.kis.kis_account import KisAccount

container = Container.get_instance()
account_repo: SqlAlchemyAccountRepository = container.account_repository()


@transactional
def refresh_kis_token():
    account_infos = account_repo.find_all(broker_type=BrokerType.KIS)

    for account_info in account_infos:
        kis_account: KisAccount = KisAccount(account_info=account_info)
        if kis_account.is_token_invalid():
            kis_account.refresh_token()
            account_repo.update(account_info)
