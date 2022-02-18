import pyupbit
import pprint

access = "KbMU00jrNHFV335NHyvHD8IvAlcg3Dgx2WrGxQJP"          # 본인 값으로 변경
secret = "2N1isooxA8Kk5kevAUiggX6pRQziFibTASahlnFQ"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

pp =pprint.PrettyPrinter()
pp.pprint(upbit.get_balances())
# print(upbit.get_balances())     # KRW-XRP 조회
# print(upbit.get_balance("KRW"))         # 보유 현금 조회
# print(upbit.get_balance("KRW-BTT")) 
# print(upbit.get_balance("KRW-VET"))
# print(upbit.get_balance("KRW-XLM"))  