import pyupbit

tickers =pyupbit.get_tickers(fiat="BTC")

print(tickers)
print(len(tickers))