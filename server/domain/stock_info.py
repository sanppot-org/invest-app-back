from typing import List


class StockInfo:
    def __init__(self, code: str, target_rate: float, rebalance_amt: int) -> None:
        self.code: str = code
        self.target_rate: float = target_rate
        self.rebalance_amt: int = rebalance_amt


class StockList:
    def __init__(self, list: List[StockInfo]) -> None:
        self.list: List[StockInfo] = list
