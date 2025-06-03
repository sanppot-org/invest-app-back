from sqlalchemy import JSON, Boolean, String, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column

from src.account.access_token import AccessToken
from src.common.infra.base_entity import BaseEntity, EnumType
from src.common.type import BrokerType


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
    __table_args__ = {"extend_existing": True}

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
