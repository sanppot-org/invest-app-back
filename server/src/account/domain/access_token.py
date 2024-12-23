from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class AccessToken:
    token: str
    expiration: str

    def is_expired(self) -> bool:
        return self._get_token_expiration() < datetime.now()

    def _get_token_expiration(self) -> datetime:
        return datetime.strptime(self.expiration, "%Y-%m-%d %H:%M:%S") - timedelta(hours=12)
