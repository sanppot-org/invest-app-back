from dataclasses import dataclass


@dataclass
class Ticker:
    value: str

    def is_crypto(self):
        return self.value.upper().startswith("KRW-")

    def get_kr_ticker(self):
        return self.value.split(".")[0]

    def is_kr(self):
        return "." in self.value
