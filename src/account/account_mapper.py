from src.account.account import Account
from src.db.account_entity import AccountEntity


class AccountMapper:
    def to_entity(self, entity: Account) -> AccountEntity:
        return AccountEntity(
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

    def to_domain(self, dto: AccountEntity) -> Account:
        return Account(
            id=dto.id,
            name=dto.name,
            app_key=dto.app_key,
            secret_key=dto.secret_key,
            broker_type=dto.broker_type,
            number=dto.number,
            product_code=dto.product_code,
            login_id=dto.login_id,
            url_base=dto.url_base,
            is_virtual=dto.is_virtual,
            token=dto.token,
        )
