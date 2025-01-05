from sqlalchemy import JSON, Boolean, String, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column
from src.account.domain.access_token import AccessToken
from src.common.domain.type import BrokerType

from src.common.adapter.out.persistence.base_entity import BaseEntity, EnumType


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
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    app_key: Mapped[str] = mapped_column(String(50))
    secret_key: Mapped[str] = mapped_column(String(100))
    broker_type: Mapped[BrokerType] = mapped_column(EnumType(BrokerType))
    number: Mapped[str] = mapped_column(String(10), nullable=True)
    product_code: Mapped[str] = mapped_column(String(2), nullable=True)
    login_id: Mapped[str] = mapped_column(String(30), nullable=True)
    url_base: Mapped[str] = mapped_column(String(100), nullable=True)
    is_virtual: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    token: Mapped[AccessToken] = mapped_column(TokenType, nullable=True)
