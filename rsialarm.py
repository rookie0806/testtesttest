import requests
import pandas as pd
import time
import webbrowser
import numpy
import time
import sys
import telegram
import pandas as pd
import requests
import pandas as pd
import sys
import time
from bs4 import BeautifulSoup
import telegram
from urllib.parse import urlencode
import os
import jwt
import uuid
import hashlib
import datetime
import requests
import requests
import datetime
import time
import sys
import numpy
import readchar
import pandas 
access_key = 'qqbypzZxyAPhKoExBDfi0vQiN5YtlhRXxX7ow52X'
secret_key = 'xDsjdKxzpqWPvFX1iFfl12QNhLym3Kfeb1x1ejYx'
server_url = 'https://api.upbit.com'
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)

symbols = ["XRP","DAWN","AERGO","DOGE","STRK","VET","HIVE","ETC","SRM","WAVES","MED","BTG","CHZ","NEO","QTUM","EOS","SC","CBK","PUNDIX","MARO","GAS","ZIL","MLK","SBD","PXL","AXS","ONT","OBSR","XEM","TRX","MVL","MOC","FLOW","DKA","ARK","MTL","TON","META","STX","SNT","MBL","XLM","TSHP","PLA","EMC2","STRAX","ADA","STMX","KMD","ORBS","PCI","CRE","IOST","SXP","DOT"] #,"MANA","STEEM","STPT","SSX","LINK","QTCON","DMT","RFR","CRO","BORA","LTC","MFT","LAMB","GRS","EDR","FCT2","AERGO","BCHA","AQT","BSV","UPP","TT"]#,"KNC","IQ","HUM","POWR","QKC","TFUEL","STORJ","HUNT","ICX","AHT","ARDR","JST","ZRX","WAXP","LSK","ONG","XTZ","KAVA","THETA","ANKR","HBAR","ENJ","OMG","REP","SAND","LBC","POLY","IGNIS","SOLVE","LOOM","CVC","GLM","ELF","ATOM","BAT","ADX","IOTA"]
buycoin = []
number = []
repeat = []
pyungdan = []
rsi_lasts = []
money = 0
moneyhap = 0
def buy(coin,price,volume):
    query = {
    'market': 'KRW-'+coin,
    'side': 'bid',
    'price': price,
    'volume': volume,
    'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    
    if(res.status_code==201):
        return True
    else:
        return False

def sell(coin,price,volume):
    query = {
    'market': 'KRW-'+coin,
    'side': 'ask',
    'price': price,
    'volume': volume,
    'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    if(res.status_code==201):
        #return float(res.json()["price"])
        return 1
    else:
        return 0

def get_my_value(coin):
    query = {
        'market': 'KRW-'+coin,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)
    balance = float(res.json()["ask_account"]["balance"])
    avg_buy_price = float(res.json()["ask_account"]["avg_buy_price"])
    return balance,avg_buy_price

for i in range(0,len(symbols)):
    buycoin.append(0)
    number.append(0)
    repeat.append(1)
    pyungdan.append(0)
    rsi_lasts.append(0)
print("working")
while True:
    for i in range(0,len(symbols)):
        try:
            time.sleep(0.5)
            url = "https://api.upbit.com/v1/candles/minutes/5"
            querystring = {"market":"KRW-"+symbols[i],"count":"500"}
            response = requests.request("GET", url, params=querystring)
            data = response.json()
            df = pd.DataFrame(data)
            df=df.reindex(index=df.index[::-1]).reset_index()
            df['close']=df["trade_price"]
            def rsi(ohlc: pd.DataFrame, period: int = 14):
                ohlc["close"] = ohlc["close"]
                delta = ohlc["close"].diff()
                up, down = delta.copy(), delta.copy()
                up[up < 0] = 0
                down[down > 0] = 0
                _gain = up.ewm(com=(period - 1), min_periods=period).mean()
                _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
                RS = _gain / _loss
                return pd.Series(100 - (100 / (1 + RS)), name="RSI")

            rsi_now = rsi(df, 14).iloc[-1]
            rsi_last = rsi(df, 14).iloc[-2]
            rsi_last2 = rsi(df, 14).iloc[-3]
            price = df["trade_price"].iloc[-1]
            
            if(rsi_lasts[i]!=rsi_last):
                if(rsi_now>=34 and rsi_now>=rsi_last2 and rsi_last<34):
                    '''
                    if(price<=100):
                        price = price-0.1
                    elif(price<=1000):
                        price = price-1
                    elif(price<=10000):
                        price = price-5
                    elif(price<=100000):
                        price = price-10
                    elif(price<=1000000):
                        price = price-50
                    ''' 
                    if(repeat[i]==1):
                        now_buy = 50000/price
                    else:
                        now_buy = 50000/price * (1 + 60*(pyungdan[i]-price)/(pyungdan[i]+price)/2)
                    number[i] = number[i] + now_buy
                    buycoin[i] = buycoin[i] + price  * now_buy
                    pyungdan[i] = buycoin[i]/number[i]
                    bot.sendMessage(chat_id = '1780594186', text="["+symbols[i]+"] ??????("+str(repeat[i])+") ?????? "+str(price)+"???, ??? ?????? :"+str(price* now_buy))
                    buy(symbols[i],price,now_buy)
                    repeat[i] = repeat[i] + 1
                mybal,my_avg_price = get_my_value(symbols[i])
                if(rsi_now>=75 and mybal!=0.0):
                    bot.sendMessage(chat_id = '1780594186', text="["+symbols[i]+"] ?????? "+str(my_avg_price)+"->"+str(price)+", ????????? : "+str(mybal*(price-my_avg_price))+"???")
                    money = money + mybal*(price-my_avg_price)
                    bot.sendMessage(chat_id = '1780594186', text="?????? ????????? : "+str(money)+"???")
                    sellbuy(symbols[i],price,now_buy)
                    number[i] = 0
                    buycoin[i] = 0
                    repeat[i] = 1
                    
                if(rsi_last>=58 and rsi_now<=rsi_last2  and mybal!=0.0):
                    if(price<=100):
                        price = price-0.1
                    elif(price<=1000):
                        price = price-1
                    elif(price<=10000):
                        price = price-5
                    elif(price<=100000):
                        price = price-10
                    elif(price<=1000000):
                        price = price-50
                    bot.sendMessage(chat_id = '1780594186', text="["+symbols[i]+"] ?????? "+str(my_avg_price)+"->"+str(price)+", ????????? : "+str(mybal*(price-my_avg_price))+"???")
                    money = money + mybal*(price-my_avg_price)
                    bot.sendMessage(chat_id = '1780594186', text="?????? ????????? : "+str(money)+"???")
                    sell(symbols[i],price,mybal)
                    number[i] = 0
                    buycoin[i] = 0
                    repeat[i] = 1
                rsi_lasts[i] = rsi_last
        except Exception as e:
            print(e)
            time.sleep(1)