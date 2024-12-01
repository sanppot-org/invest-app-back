from typing import List


class StockInfo:
    def __init__(self, code: str, target_rate: float, rebalance_amt: int = 0):
        self.code: str = code
        self.target_rate: float = target_rate
        self.rebalance_amt: int = rebalance_amt

    def to_dict(self):
        return {
            "code": self.code,
            "target_rate": self.target_rate,
            "rebalance_amt": self.rebalance_amt,
        }


class StockList:
    def __init__(self, list: List[StockInfo]):
        self.list: List[StockInfo] = list
