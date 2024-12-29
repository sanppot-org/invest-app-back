from dataclasses import dataclass

from src.common.domain.exception import ExeptionType, InvestAppException


@dataclass
class Ticker:
    value: str

    def validate_crypto_ticker(self):
        if not self.is_crypto():
            raise InvestAppException(ExeptionType.INVALID_TICKER, self.value)

    def is_crypto(self):
        return self.value.upper().startswith("KRW-")

    def get_kr_ticker(self):
        return self.value.split(".")[0]

    def is_kr(self):
        return "." in self.value
