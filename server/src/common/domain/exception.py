from sqlalchemy import Enum


class ExeptionType(Enum):
    ENTITY_NOT_FOUND = ["엔티티가 없습니다. id: {}", 400]
    INVALID_ACCOUNT_TYPE = ["지원하지 않는 계좌 종류입니다. type: {}", 400]
    FAILED_TO_CREATE_TOKEN = ["토큰 생성 실패. {}", 500]
    FAILED_TO_GET_BALANCE = ["잔고 조회 실패. {}", 500]
    FAILED_TO_GET_CURRENT_PRICE = ["현재가 조회 실패. {}", 500]
    NOT_TIME_TO_REBALANCE = ["리밸런싱 조건이 아닙니다. {}", 400]
    MARKET_NOT_OPEN = ["주식 시장이 열리지 않았습니다. {}", 400]
    INVALID_PORTFOLIO_RATE = ["포트폴리오 종목 비중의 합은 1이어야 합니다. {}", 400]


class InvestAppException(Exception):
    def __init__(self, exception_type: ExeptionType, *args):
        self.error_code = exception_type[1]
        self.message = exception_type[0].format(*args) if args else exception_type[0]
