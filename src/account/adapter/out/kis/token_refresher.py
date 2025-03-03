from src.account.application.port.out.account_repository import AccountRepository
from src.containers import Container
from src.common.domain.type import BrokerType
from src.account.adapter.out.kis.kis_account import KisAccount
from dependency_injector.wiring import inject, Provide


@inject
def refresh_kis_token(account_repo: AccountRepository = Provide[Container.account_repository]):
    account_infos = account_repo.find_all(broker_type=BrokerType.KIS)

    for account_info in account_infos:
        kis_account: KisAccount = KisAccount(account_info=account_info)
        if kis_account.is_token_invalid():
            kis_account.refresh_token()

    account_repo.upsert_all(account_infos)
