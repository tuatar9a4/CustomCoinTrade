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
# my_wallet_code =upbit.get_balances()
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
def upDownCoount(code="KRW-BTC",current=0):
    df = pyupbit.get_ohlcv(code, interval="minute5", count=2)
    for b in range(1,len(df)) :
        # 현재 - 과거
        if((((current-df.iloc[b]['close'])/df.iloc[b]['close'])*100)>2):
           return "don't sell"

def cloesVsCurrent(code="KRW-BTC",current=0):
    df = pyupbit.get_ohlcv(code, interval="minute60", count=2)
    print("==cloesVsCurrent==")
    print("current")
    print(current)
    # 종가 - 현재가랑 마이너스가 4퍼 이상나면 팔기
    print("float(df.iloc[b]['close'])")
    print(float(df.iloc[0]['close']))
    if(current<float(df.iloc[0]['close'])):
        return "sell"
    else:
        return "none"

# 구매 
def getTarget(code="KRW-BTC",k=0.5) :
    """변동성 돌파 전략으로 매수 목표가 조회"""
    timeBong = pyupbit.get_ohlcv(code, interval="minute60", count=2)
    target = timeBong.iloc[0]['close'] + (timeBong.iloc[0]['high'] - timeBong.iloc[0]['low']) * k
    return target


#코인 매수 평균알기
def myAverage(code="KRW-BTC"):
    codeSplit=code.split("-")
    myCoins =upbit.get_balances()
    for coin in myCoins:
        if(coin["currency"]==codeSplit[1]):
            return float(coin["avg_buy_price"])
            break

# 자동매매 시작
targetCoin="KRW-ZRX"
while True:

    # try:
        currentTime = datetime.datetime.now()
        startTime = get_start_time(targetCoin)
        endTime = startTime + datetime.timedelta(days=1)
        currentPrice = get_current_price(targetCoin)

        if startTime < currentTime < endTime - datetime.timedelta(seconds=10):
            targetPrice = getTarget(targetCoin, 0.5)
            print("===구매===")
            print("targetPrice")
            print(targetPrice)
            print("currentPrice")
            print(currentPrice)
            if targetPrice < currentPrice:
                myAccount = get_balance("KRW")
                print("myAccount")
                print(myAccount)
                if myAccount > 5000:
                    upbit.buy_market_order(targetCoin, myAccount*0.9995)
                    # pass
        else:
            pass
        myCoins=upbit.get_balance(targetCoin)
        if upDownCoount(targetCoin,currentPrice)=="don't sell":
            # 5퍼 이상으로 올랐으면 안팜 
            pass
        elif (myCoins>(currentPrice/5000)*0.98):
            # 팔수있음
            print("==판매==")
            print("currentPrice")
            print(currentPrice)
            print("myCoins")
            print(myCoins)
            print("myAverage(targetCoin)")
            print(myAverage(targetCoin))
            if (currentPrice*myCoins)>(myCoins*myAverage(targetCoin)*1.15) :
                # 15퍼 이상 이득일때 팔고
                upbit.sell_market_order(targetCoin, myCoins*0.9995)
                pass
            elif(cloesVsCurrent(targetCoin,currentPrice)=="sell"):
                # 샀는데 올른후 거기에서 가격이 떨어지면 팔자 
                upbit.sell_market_order(targetCoin, myCoins*0.9995)
                pass
            elif ((myCoins*myAverage(targetCoin))*0.96>currentPrice*myCoins) :
                # 지금 내가 산 총 금액 
                upbit.sell_market_order(targetCoin, myCoins*0.9995)
                pass
        print("거래중...")
        time.sleep(1)
    # except Exception as e:
    #     print(e)
    #     time.sleep(1)