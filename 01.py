from numpy import append
import requests

uri = "https://api.upbit.com/v1/market/all"
params = {
    "isDetails":"true"
}

resp = requests.get(uri,params)
data =resp.json()
# print(data)

kr_tikers =[]
for coin in data:
    ticker = coin['market']
    if(ticker.startswith("KRW")): {
        kr_tikers.append(ticker)
    }
    
print(kr_tikers)
print(len(kr_tikers))

