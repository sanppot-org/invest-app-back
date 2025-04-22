from sqlalchemy import JSON, Boolean, String, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column
from src.account.access_token import AccessToken
from src.common.type import BrokerType
from src.db.base_entity import BaseEntity, EnumType


class TokenType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value: AccessToken, dialect):
        if value is not None:
            return {
                "token": value.token,
                "expiration": value.expiration,
            }
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return AccessToken(**value)
        return None


class AccountEntity(BaseEntity):
    __tablename__ = "account"
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    app_key: Mapped[str] = mapped_column(String(50), nullable=False)
    secret_key: Mapped[str] = mapped_column(String(100), nullable=False)
    broker_type: Mapped[BrokerType] = mapped_column(EnumType(BrokerType, length=5), nullable=False)
    number: Mapped[str] = mapped_column(String(10), nullable=True)
    product_code: Mapped[str] = mapped_column(String(2), nullable=True)
    login_id: Mapped[str] = mapped_column(String(30), nullable=True)
    url_base: Mapped[str] = mapped_column(String(100), nullable=True)
    is_virtual: Mapped[bool] = mapped_column(Boolean, nullable=False)
    token: Mapped[AccessToken] = mapped_column(TokenType, nullable=True)

    def update(self, entity: "AccountEntity"):
        self.name = entity.name
        self.app_key = entity.app_key
        self.secret_key = entity.secret_key
        self.broker_type = entity.broker_type
        self.number = entity.number
        self.product_code = entity.product_code
        self.login_id = entity.login_id
        self.url_base = entity.url_base
        self.is_virtual = entity.is_virtual
        self.token = entity.token
