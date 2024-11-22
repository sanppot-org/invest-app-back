from typing import Optional
from pydantic import BaseModel


class StrategyCreateReq(BaseModel):
    name: str
    invest_rate: Optional[float] = None
    env: Optional[str] = None


class StrategyUpdateReq(BaseModel):
    name: str
    invest_rate: Optional[float] = None
    env: Optional[str] = None
