import pyupbit
import numpy as np


# OHLCV(open,high,low,close,vloume) 로 당일 시가,고사,저가,종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC",count=7)
# 변동성 돌파 기준 범위 계산, (고강 - 저가) *k
df['range'] = (df['high'] - df['low']) * 0.8
# range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# np.where(조건문, 참일때 값, 거짓일때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

#누적 곱 계산 => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# 하락폭 
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#MDD
print("MDD(%): ", df['dd'].max())
#엑셀로 출력
df.to_excel("dd.xlsx")