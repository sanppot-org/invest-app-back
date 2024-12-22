from dataclasses import dataclass
from datetime import datetime

from src.common.repository import Repository
from src.common.type import BrokerType


@dataclass
class AccessToken:
    token: str
    expiration: datetime


@dataclass
class AccountInfo:
    id: int
    name: str
    app_key: str
    secret_key: str
    broker_type: BrokerType
    number: str
    product_code: str
    login_id: str
    url_base: str
    is_virtual: bool
    token: AccessToken


class AccountRepository(Repository[AccountInfo]):
    pass
