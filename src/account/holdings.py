class Holdings:
    """
    보유 종목
    """

    def __init__(self, name: str, code: str, quantity: float, avg_price: float, eval_amt: float):
        self.name = name  # 종목명
        self.code = code  # 종목코드
        self.quantity = quantity  # 보유수량
        self.avg_price = avg_price  # 평균매수가
        self.eval_amt = eval_amt  # 평가금액

    def __str__(self) -> str:
        return f"name: {self.name}, code: {self.code}, quantity: {self.quantity:.8f}, avg_price: {self.avg_price:.4f}, eval_amt: {self.eval_amt:.4f}"

    def __repr__(self) -> str:
        return self.__str__()
