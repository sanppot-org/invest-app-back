# 투자 주식 설정

# 전략 이름
# 계좌 선택 (목록에서 동적으로 수정 가능)
# 전략 할당 비중, 금액 설정
# 투자 주식 설정 (종목, 비중)
# 스케줄러 설정

from pydantic import BaseModel
from typing import List, Optional
from domain.env.env_type import EnvType
from domain.stock_info import StockInfo


class StrategyCreateRequest(BaseModel):
    name: str
    env: Optional[EnvType] = EnvType.REAL
    weight: float
    stock_list: List[StockInfo]
