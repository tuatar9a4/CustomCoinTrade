import time
import pyupbit
import datetime

access = "KbMU00jrNHFV335NHyvHD8IvAlcg3Dgx2WrGxQJP"
secret = "2N1isooxA8Kk5kevAUiggX6pRQziFibTASahlnFQ"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 내 현금 
# 내잔고 = get_balance("KRW")
# print("krw : ",내잔고)
# btc = get_balance("KRW-BTC")
# print("btc : " ,btc)

# print("내 지갑의 코인 코드")
my_wallet_code =upbit.get_balances()
# for my in my_wallet_code :
#     myCode=my['unit_currency']+"-"+my['currency']
#     try:
#         currentCost =str(pyupbit.get_current_price("KRW-STORJ"))
#         print("=========="+my['unit_currency']+"-"+my['currency']+"==========")
#         print("내 매수 평균 : "+my['avg_buy_price'] +"|| 개수 "+my['balance'])
#         print("현재 체결가 : "+currentCost)
#         df = pyupbit.get_ohlcv(myCode, interval="minute1", count=10)
#         print(df)
#     except  :
#         pass

# btc = upbit.get_balance("KRW-KNC")
# 지금_가격 = get_current_price("KRW-KNC")
# print("btc : " ,지금_가격)

# 현재_체결가 =str(pyupbit.get_current_price("KRW-MOC"))
# print("현재 체결가 : "+현재_체결가)
# print(df.iloc[0]) #0이 더 느린시간
# print(df.iloc[1])

# 하락장 상승장 파악
def getmount(code="KRW-BTC"):
    df = pyupbit.get_ohlcv(code, interval="minute5", count=10)
    upCnt=0
    downCnt=0
    for b in range(1,len(df)) :
        # 현재 - 과거
        if(df.iloc[b-1]['open']<df.iloc[b]['high']) :
            # 하락
            downCnt+=1
            pass
        else :
            upCnt+=1
            #상승
    if(downCnt>upCnt):
        return "down"
    else:
        return "up"
    
#상승률 하락률
def 상승하락률계산(code="KRW-BTC",현재가=0):
    df = pyupbit.get_ohlcv(code, interval="minute5", count=2)
    for b in range(1,len(df)) :
        # 현재 - 과거
        if((((현재가-df.iloc[b]['close'])/df.iloc[b]['close'])*100)>2):
            return "팔지마"

def 장종료가랑_비교(code="KRW-BTC",현재가=0):
     df = pyupbit.get_ohlcv(code, interval="minute60", count=2)
     for b in range(1,len(df)) :
        # 종가 - 현재가랑 마이너스가 4퍼 이상나면 팔기
        if((((현재가-df.iloc[b]['close'])/df.iloc[b]['close'])*100)<-4):
            return "팔아"

# 구매 
def 목표가확인(code="KRW-BTC",k=0.5) :
    """변동성 돌파 전략으로 매수 목표가 조회"""
    시간봉 = pyupbit.get_ohlcv(code, interval="minute60", count=2)
    체결가 = 시간봉.iloc[0]['close'] + (시간봉.iloc[0]['high'] - 시간봉.iloc[0]['low']) * k
    return 체결가

#코인 매수 평균알기
def 코인_매수_평균_계산(code="KRW-BTC"):
    코드분석=code.split("-")
    내보유코인 =upbit.get_balances()
    for 코인 in 내보유코인:
        if(코인["currency"]==코드분석[1]):
            print(코인["avg_buy_price"])
            return 코인["avg_buy_price"]
            break

# 자동매매 시작
매매할_코인_이름="KRW-KNC"
while True:

    try:
        지금시간 = datetime.datetime.now()
        시작시간 = get_start_time(매매할_코인_이름)
        끝나는시간 = 시작시간 + datetime.timedelta(days=1)
        지금_가격 = get_current_price(매매할_코인_이름)

        if 시작시간 < 지금시간 < 끝나는시간 - datetime.timedelta(seconds=10):
            목표가 = 목표가확인(매매할_코인_이름, 0.5)
            if 목표가 < 지금_가격:
                내잔고 = get_balance("KRW")
                if 내잔고 > 5000:
                    upbit.buy_market_order(매매할_코인_이름, 내잔고*0.9995)
        else:
            pass
        내_코인_수=upbit.get_balance(매매할_코인_이름)
        if 상승하락률계산(매매할_코인_이름,지금_가격)=="팔지마":
            # 5퍼 이상으로 올랐으면 안팜 
            pass
        elif (내_코인_수>(지금_가격/5000)*0.98):
            # 팔수있음
            if (지금_가격*내_코인_수>내_코인_수*코인_매수_평균_계산(매매할_코인_이름))*1.15 :
                # 15퍼 이상 이득일때 팔고
                upbit.sell_market_order(매매할_코인_이름, 내_코인_수*0.9995)
                pass
            elif(장종료가랑_비교(매매할_코인_이름,지금_가격)=="팔아"):
                # 샀는데 올른후 거기에서 가격이 떨어지면 팔자 
                upbit.sell_market_order(매매할_코인_이름, 내_코인_수*0.9995)
                pass
            elif ((내_코인_수*코인_매수_평균_계산(매매할_코인_이름))*0.95<지금_가격*내_코인_수) :
                # 지금 내가 산 총 금액 
                upbit.sell_market_order(매매할_코인_이름, 내_코인_수*0.9995)
                pass
        print("거래중...")
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)