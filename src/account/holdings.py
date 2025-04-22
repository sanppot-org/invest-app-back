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
