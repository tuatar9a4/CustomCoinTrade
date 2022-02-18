import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC","days")
# open 시가  hight 고가 low 저가  close 종가  volume 거래량  value 거래금액 
# print(df)

redfOpen = df['open'].resample('3D').first()
redfHigh = df['high'].resample('3T').max()
redfLow = df['low'].resample('3T').min()
redfClose = df['close'].resample('3T').last()
redfVolum = df['volume'].resample('3T').sum()
redfValue = df['value'].resample('3T').sum()

print(redfOpen)