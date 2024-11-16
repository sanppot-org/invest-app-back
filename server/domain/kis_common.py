import json
import requests
from datetime import datetime, timedelta
from pytz import timezone
import domain.kis_api_helper_us as kis_us
import domain.kis_api_helper_kr as kis_kr
import time
import FinanceDataReader as fdr
import pandas_datareader.data as web
import pandas as pd
from domain.env.env_type import EnvType
import domain.env.env as env

############################################################################################################################################################
NOW_DIST: EnvType = EnvType.REAL


# 계좌 전환 함수! REAL 실계좌 VIRTUAL 모의계좌
def set_change_mode(dist: EnvType = EnvType.REAL):
    global NOW_DIST
    NOW_DIST = dist


# 현재 선택된 계좌정보를 리턴!
def get_now_dist():
    return NOW_DIST


############################################################################################################################################################


# 토큰 값을 리퀘스트 해서 실제로 만들어서 파일에 저장하는 함수!! 첫번째 파라미터: "REAL" 실계좌, "VIRTUAL" 모의계좌
def make_token():
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": env.get_app_key(),
        "appsecret": env.get_app_secret(),
    }

    PATH = "oauth2/tokenP"
    URL = f"{env.get_url_base()}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code == 200:
        my_token = res.json()["access_token"]

        # 빈 딕셔너리를 선언합니다!
        dataDict = dict()

        # 해당 토큰을 파일로 저장해 둡니다!
        dataDict["authorization"] = my_token
        with open(env.get_token_path(), "w") as outfile:
            json.dump(dataDict, outfile)
        print("TOKEN : ", my_token)
        return my_token
    else:
        print("Get Authentification token fail!")
        return "FAIL"


# 파일에 저장된 토큰값을 읽는 함수.. 만약 파일이 없다면 make_token 함수를 호출한다!
def get_token():
    # 빈 딕셔너리를 선언합니다!
    dataDict = dict()
    try:
        # 이 부분이 파일을 읽어서 딕셔너리에 넣어주는 로직입니다.
        with open(env.get_token_path(), "r") as json_file:
            dataDict = json.load(json_file)
        return dataDict["authorization"]
    except Exception as e:
        print("Exception by First")
        # 처음에는 파일이 존재하지 않을테니깐 바로 토큰 값을 구해서 리턴!
        return make_token()


############################################################################################################################################################
# 해시키를 리턴한다!
def get_hash_key(datas):
    PATH = "uapi/hashkey"
    URL = f"{env.get_url_base(NOW_DIST)}/{PATH}"

    headers = {
        "content-Type": "application/json",
        "appKey": env.get_app_key(NOW_DIST),
        "appSecret": env.get_app_secret(NOW_DIST),
    }

    res = requests.post(URL, headers=headers, data=json.dumps(datas))

    if res.status_code == 200:
        return res.json()["HASH"]
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


############################################################################################################################################################
# 한국인지 미국인지 구분해 현재 날짜정보를 리턴해 줍니다!
def get_now_date_str(area="KR", type="NONE"):
    timezone_info = timezone("Asia/Seoul")
    if area == "US":
        timezone_info = timezone("America/New_York")

    now = datetime.now(timezone_info)
    if type.upper() == "NONE":
        return now.strftime("%Y%m%d")
    else:
        return now.strftime("%Y-%m-%d")


# 현재날짜에서 이전/이후 날짜를 구해서 리턴! (미래의 날짜를 구할 일은 없겠지만..)
def get_from_now_date_str(area="KR", type="NONE", days=100):
    timezone_info = timezone("Asia/Seoul")
    if area == "US":
        timezone_info = timezone("America/New_York")

    now = datetime.now(timezone_info)

    if days < 0:
        next = now - timedelta(days=abs(days))
    else:
        next = now + timedelta(days=days)

    if type.upper() == "NONE":
        return next.strftime("%Y%m%d")
    else:
        return next.strftime("%Y-%m-%d")


############################################################################################################################################################


# 통합 증거금 사용시 잔고 확인!
def get_balance_krw_total():
    kr_data = kis_kr.get_balance()
    us_data = kis_us.get_balance("KRW")

    balanceDict = dict()

    balanceDict["RemainMoney"] = str(
        float(kr_data["RemainMoney"]) + float(us_data["RemainMoney"])
    )
    # 주식 총 평가 금액
    balanceDict["StockMoney"] = str(
        float(kr_data["StockMoney"]) + float(us_data["StockMoney"])
    )
    # 평가 손익 금액
    balanceDict["StockRevenue"] = str(
        float(kr_data["StockRevenue"]) + float(us_data["StockRevenue"])
    )
    # 총 평가 금액
    balanceDict["total_money"] = str(
        float(kr_data["total_money"]) + float(us_data["total_money"])
    )

    return balanceDict


############################################################################################################################################################
# OHLCV 값을 한국투자증권 혹은 FinanceDataReader 혹은 야후 파이낸스에서 가지고 옴!
def get_ohlcv(area, stock_code, limit=500):

    Adjlimit = (
        limit * 1.7
    )  # 주말을 감안하면 5개를 가져오려면 적어도 7개는 뒤져야 된다. 1.4가 이상적이지만 혹시 모를 연속 공휴일 있을지 모르므로 1.7로 보정해준다

    df = None

    except_riase = False

    try:

        if area == "US":

            print("----First try----")
            df = kis_us.get_ohlcv(stock_code, "D")

            # 한투에서 100개 이상 못가져 오니깐 그 이상은 아래 로직을 탄다. 혹은 없는 종목이라면 역시 아래 로직을 탄다
            if Adjlimit > 100 or len(df) == 0:

                # 미국은 보다 빠른 야후부터
                except_riase = False
                try:
                    print("----Second try----")
                    df = get_ohlcv2(area, stock_code, Adjlimit)
                except Exception as e:
                    except_riase = True

                if except_riase == True:
                    print("----Third try----")
                    df = get_ohlcv1(area, stock_code, Adjlimit)

        else:

            print("----First try----")
            df = kis_kr.get_ohlcv(stock_code, "D")

            # 한투에서 100개 이상 못가져 오니깐 그 이상은 아래 로직을 탄다. 혹은 없는 종목이라면 역시 아래 로직을 탄다
            if Adjlimit > 100 or len(df) == 0:

                # 한국은 KRX 정보데이터시스템 부터
                except_riase = False
                try:
                    print("----Second try----")
                    df = get_ohlcv1(area, stock_code, Adjlimit)
                except Exception as e:
                    except_riase = True

                if except_riase == True:
                    print("----Third try----")
                    df = get_ohlcv2(area, stock_code, Adjlimit)

    except Exception as e:
        print(e)
        except_riase = True

    if except_riase == True:
        return df
    else:
        print("---", limit)
        return df[-limit:]


# 한국 주식은 KRX 정보데이터시스템에서 가져온다. 그런데 미국주식 크롤링의 경우 investing.com 에서 가져오는데 안전하게 2초 정도 쉬어야 한다!
# https://financedata.github.io/posts/finance-data-reader-users-guide.html
def get_ohlcv1(area, stock_code, limit=500):

    df = fdr.DataReader(
        stock_code,
        get_from_now_date_str(area, "BAR", -limit),
        get_now_date_str(area, "BAR"),
    )

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index.name = "Date"

    # 거래량과 시가,종가,저가,고가의 평균을 곱해 대략의 거래대금을 구해서 value 라는 항목에 넣는다 ㅎ
    df.insert(
        5,
        "value",
        ((df["open"] + df["high"] + df["low"] + df["close"]) / 4.0) * df["volume"],
    )

    df.insert(6, "change", (df["close"] - df["close"].shift(1)) / df["close"].shift(1))

    df[["open", "high", "low", "close", "volume", "change"]] = df[
        ["open", "high", "low", "close", "volume", "change"]
    ].apply(pd.to_numeric)

    # 미국주식은 2초를 쉬어주자! 안그러면 24시간 정지당할 수 있다!
    if area == "US":
        time.sleep(2.0)
    else:
        time.sleep(0.2)

    return df


# 야후 파이낸스에서 정보 가져오기!
# https://pandas-datareader.readthedocs.io/en/latest/
def get_ohlcv2(area, stock_code, limit=500):

    df = None

    if area == "KR":

        except_riase = False
        try:
            df = web.DataReader(
                stock_code + ".KS",
                "yahoo",
                get_from_now_date_str(area, "BAR", -limit),
                get_now_date_str(area, "BAR"),
            )
        except Exception as e:
            except_riase = True

        if except_riase == True:
            try:
                df = web.DataReader(
                    stock_code + ".KQ",
                    "yahoo",
                    get_from_now_date_str(area, "BAR", -limit),
                    get_now_date_str(area, "BAR"),
                )
            except Exception as e:
                print("")

    else:
        df = web.DataReader(
            stock_code,
            "yahoo",
            get_from_now_date_str(area, "BAR", -limit),
            get_now_date_str(area, "BAR"),
        )

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index.name = "Date"

    # 거래량과 시가,종가,저가,고가의 평균을 곱해 대략의 거래대금을 구해서 value 라는 항목에 넣는다 ㅎ
    df.insert(
        5,
        "value",
        ((df["open"] + df["high"] + df["low"] + df["close"]) / 4.0) * df["volume"],
    )

    df.insert(6, "change", (df["close"] - df["close"].shift(1)) / df["close"].shift(1))

    df[["open", "high", "low", "close", "volume", "change"]] = df[
        ["open", "high", "low", "close", "volume", "change"]
    ].apply(pd.to_numeric)

    time.sleep(0.2)

    return df


############################################################################################################################################################


# 이동평균선 수치를 구해준다 첫번째: 일봉 정보, 두번째: 기간, 세번째: 기준 날짜
def get_ma(ohlcv, period, st):
    close = ohlcv["close"]
    ma = close.rolling(period).mean()
    return float(ma.iloc[st])
