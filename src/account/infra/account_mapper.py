from src.db.entity_mapper import EntityMapper
from src.account.account import Account
from src.account.infra.account_entity import AccountEntity


class AccountMapper(EntityMapper[Account, AccountEntity]):
    def to_entity(self, domain: Account) -> AccountEntity:
        return AccountEntity(
            id=domain.id,
            name=domain.name,
            app_key=domain.app_key,
            secret_key=domain.secret_key,
            broker_type=domain.broker_type,
            number=domain.number,
            product_code=domain.product_code,
            login_id=domain.login_id,
            url_base=domain.url_base,
            is_virtual=domain.is_virtual,
            token=domain.token,
        )

    def to_domain(self, entity: AccountEntity) -> Account:
        return Account(
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
