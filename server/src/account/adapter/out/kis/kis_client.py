import json
import requests
from src.account.domain.access_token import AccessToken
from src.common.domain.exception import ExeptionType, InvestAppException
from src.account.adapter.out.kis.dto import BalanceResponse, KisInfo, KisInfoForToken
import yfinance as yf

from src.common.domain.type import Market
from src.common.domain.config import logger


def get_token(info: KisInfoForToken) -> AccessToken | None:
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": info.app_key,
        "appsecret": info.secret_key,
    }
    URL = f"{info.url_base}/oauth2/tokenP"

    try:
        res = requests.post(URL, headers=headers, data=json.dumps(body))
    except Exception as e:
        logger.error(f"Failed to create token: {e}")
        return None

    if res.status_code != 200:
        raise InvestAppException(ExeptionType.FAILED_TO_CREATE_TOKEN, res.text)

    res_body = res.json()
    return AccessToken(token=res_body["access_token"], expiration=res_body["access_token_token_expired"])


def get_balance(info: KisInfo, market: Market = Market.KR) -> float:
    if market == Market.KR:
        return BalanceResponse.of(_get_balance_kr(info).json()["output2"][0]).total_money

    return _get_balance_us(info)


def get_stocks(info: KisInfo):
    res = _get_balance_kr(info)

    return res.json()["output1"]


def _get_balance_kr(info: KisInfo):
    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "TTTC8434R" if info.is_real else "VTTC8434R",
        "custtype": "P",
    }

    params = {
        "CANO": info.account_number,
        "ACNT_PRDT_CD": info.product_code,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": "",
    }

    URL = f"{info.url_base}/uapi/domestic-stock/v1/trading/inquire-balance"

    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return res

    raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, res.text)


def _get_balance_us(info: KisInfo):
    URL = f"{info.url_base}/uapi/overseas-stock/v1/trading/inquire-present-balance"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "CTRP6504R" if info.is_real else "VTRP6504R",
        "custtype": "P",
    }

    params = {
        "CANO": info.account_number,
        "ACNT_PRDT_CD": info.product_code,
        "WCRC_FRCR_DVSN_CD": "02",
        "NATN_CD": "840",
        "TR_MKET_CD": "00",
        "INQR_DVSN_CD": "00",
    }

    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        result = res.json()["output2"]
        return result

        # # 실시간 주식 상태가 반영이 안되서 주식 정보를 직접 읽어서 계산!
        # my_stock_list = GetMyStockList(st)

        # StockOriMoneyTotal = 0
        # StockNowMoneyTotal = 0

        # for stock in my_stock_list:
        #     # pprint.pprint(stock)
        #     StockOriMoneyTotal += float(stock["StockOriMoney"])
        #     StockNowMoneyTotal += float(stock["StockNowMoney"])

        #     # print("--", StockNowMoneyTotal, StockOriMoneyTotal)

        # balanceDict = dict()
        # balanceDict["RemainMoney"] = 0

        # Rate = 1200

        # if st == "USD":

        #     for data in result:
        #         if data["crcy_cd"] == "USD":
        #             # 예수금 총금액 (즉 주문가능 금액)
        #             balanceDict["RemainMoney"] = (
        #                 float(data["frcr_dncl_amt_2"])
        #                 - float(data["frcr_buy_amt_smtl"])
        #                 + float(data["frcr_sll_amt_smtl"])
        #             )  # 모의계좌는 0으로 나온다 이유는 모르겠음!
        #             Rate = data["frst_bltn_exrt"]
        #             break

        #     result = res.json()["output3"]

        #     # 임시로 모의 계좌 잔고가 0으로
        #     if (
        #         common.GetNowDist() == "VIRTUAL"
        #         and float(balanceDict["RemainMoney"]) == 0
        #     ):

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"]) / float(
        #             Rate
        #         )

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        #     else:

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        # else:

        #     for data in result:
        #         if data["crcy_cd"] == "USD":
        #             Rate = data["frst_bltn_exrt"]
        #             # 예수금 총금액 (즉 주문가능현금)
        #             balanceDict["RemainMoney"] = (
        #                 float(data["frcr_dncl_amt_2"])
        #                 - float(data["frcr_buy_amt_smtl"])
        #                 + float(data["frcr_sll_amt_smtl"])
        #             ) * float(Rate)
        #             # balanceDict['RemainMoney'] = data['frcr_evlu_amt2'] #모의계좌는 0으로 나온다 이유는 모르겠음!

        #             break

        #     # print("balanceDict['RemainMoney'] ", balanceDict['RemainMoney'] )

        #     result = res.json()["output3"]

        #     # 임시로 모의 계좌 잔고가 0으로 나오면
        #     if (
        #         common.GetNowDist() == "VIRTUAL"
        #         and float(balanceDict["RemainMoney"]) == 0
        #     ):

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"])

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        #     else:

        #         # 주식 총 평가 금액
        #         balanceDict["stock_money"] = (
        #             StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
        #         )
        #         # 평가 손익 금액
        #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
        #             StockOriMoneyTotal
        #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

        #         # 총 평가 금액
        #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
        #             balanceDict["RemainMoney"]
        #         )

        # return balanceDict

    raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, res.text)


def get_current_price(info: KisInfo, ticker: str) -> float:
    if ticker.isdigit():
        return _get_current_price_kr(info, ticker)

    return _get_current_price_us(ticker)


def _get_current_price_kr(info: KisInfo, ticker: str) -> float:
    URL = f"{info.url_base}/uapi/domestic-stock/v1/quotations/inquire-price"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "FHKST01010100",
    }

    params = {"FID_COND_MRKT_DIV_CODE": "J", "FID_INPUT_ISCD": ticker}

    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        return int(res.json()["output"]["stck_prpr"])

    raise InvestAppException(ExeptionType.FAILED_TO_GET_CURRENT_PRICE, res.text)


def _get_current_price_us(ticker: str) -> float:
    stock = yf.Ticker(ticker)

    latest_data = stock.history(period="1d", interval="1m")

    return latest_data.iloc[-1]["Close"]


def buy_market_order_us(info: KisInfo, ticker: str, amount: float):
    price = get_current_price(info, ticker) * 1.1
    return buy_limit_order_us(info, ticker, amount, price)


def buy_limit_order_us(info: KisInfo, ticker: str, amount: float, price: float):
    # 가상 계좌는 해외 주식 거래 불가
    URL = f"{info.url_base}/uapi/overseas-stock/v1/trading/order"

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {info.token}",
        "appKey": info.app_key,
        "appSecret": info.secret_key,
        "tr_id": "JTTT1002U" if info.is_real else "VTTT1002U",
        "custtype": "P",
    }

    data = {
        "CANO": info.account_number,
        "ACNT_PRDT_CD": info.product_code,
        "OVRS_EXCG_CD": "NYSE",
        "PDNO": ticker,
        "ORD_DVSN": "00",
        "ORD_QTY": str(int(amount)),
        "OVRS_ORD_UNPR": str(price),
        "ORD_SVR_DVSN_CD": "0",
    }

    res = requests.post(URL, headers=headers, data=json.dumps(data))

    print(res.json())

    if res.status_code == 200 and res.json()["rt_cd"] == "0":
        order = res.json()["output"]

        OrderInfo = dict()

        OrderInfo["OrderNum"] = order["KRX_FWDG_ORD_ORGNO"]
        OrderInfo["OrderNum2"] = order["ODNO"]
        OrderInfo["OrderTime"] = order["ORD_TMD"]

        return OrderInfo


def sell_market_order(info: KisInfo, ticker: str, amount: float):
    pass
