from src.containers import Container
from src.common.domain.type import BrokerType
from src.account.adapter.out.kis import kis_client
from src.account.domain.access_token import AccessToken
from src.account.adapter.out.kis.kis_account import KisAccount

container = Container.get_instance()
account_repo = container.account_repository()


def refresh_kis_token():
    account_dtos = account_repo.find_all(broker_type=BrokerType.KIS)

    for account_dto in account_dtos:
        kis_account: KisAccount = KisAccount(account_dto=account_dto)
        if kis_account.is_token_invalid():
            account_dto.token = kis_client.get_token(kis_account.get_kis_info_for_token())

    account_repo.upsert_all(account_dtos)
