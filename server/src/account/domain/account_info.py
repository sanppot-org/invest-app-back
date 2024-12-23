from dataclasses import dataclass
from src.domain.common.type import BrokerType
from src.account.domain.access_token import AccessToken


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
