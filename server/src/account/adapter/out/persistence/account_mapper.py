from src.account.domain.account_create_command import AccountCreateCommand
from src.account.adapter.out.kis.kis_account import KisAccount
from src.account.adapter.out.persistence.account_entity import AccountEntity
from src.account.domain.account_info import AccountInfo


class AccountMapper:
    def to_entity(self, dto: AccountCreateCommand) -> AccountEntity:
        return AccountEntity(
            name=dto.name,
            app_key=dto.app_key,
            secret_key=dto.secret_key,
            broker_type=dto.broker_type,
            number=dto.number,
            product_code=dto.product_code,
            login_id=dto.login_id,
            url_base=dto.url_base,
            is_virtual=dto.is_virtual,
        )

    def to_model(self, entity: AccountEntity) -> AccountInfo:
        return AccountInfo(
            id=entity.id,
            name=entity.name,
            app_key=entity.app_key,
            secret_key=entity.secret_key,
            broker_type=entity.broker_type,
            number=entity.number,
            product_code=entity.product_code,
            login_id=entity.login_id,
            url_base=entity.url_base,
            is_virtual=entity.is_virtual,
            token=entity.token,
        )

    def to_kis_domain(self, entity: AccountEntity) -> KisAccount:
        return KisAccount(account_info=entity, is_virtual=entity.is_virtual)
