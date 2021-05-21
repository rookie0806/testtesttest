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
import pyupbit
access_key = 'qqbypzZxyAPhKoExBDfi0vQiN5YtlhRXxX7ow52X'
secret_key = 'xDsjdKxzpqWPvFX1iFfl12QNhLym3Kfeb1x1ejYx'
server_url = 'https://api.upbit.com'
upbit = pyupbit.Upbit(access_key, secret_key)
#code = ["XRP","DAWN","DOGE","STRK","ETC","SRM","WAVES","BTG","NEO","QTUM","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
#code = ["ETH","QTUM","BTC","XRP","EOS","BCH","BTT","ADA","LTC","KMD","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
#code = ["BTT","MBL","AHT","TT","MFT","CRE","RFR","TSHP","IQ","MVL","OBSR","QKC","SC","STMX","EDR","IOST","QTCON","LAMB","STPT"]
code = ["BTC","ETH","BCH","LTC","BSV","ETC","BTG","NEO","STRK","LINK","REP","DOT","BCHA","WAVES","ATOM","FLOW","QTUM","SBD","GAS"]
buyflag = []
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)
hap = 0
money = 20000000
cnt = 0

def buy(coin,volume,price):
    query = {
    'market': 'KRW-'+coin,
    'side': 'bid',
    'price': price,
    'volume': '',
    'ord_type': 'price',
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
    print(res.text)
    if(res.status_code==201):
        return True
    else:
        return False

def sell(coin,volume,price):
    query = {
    'market': 'KRW-'+coin,
    'side': 'ask',
    'price': '',
    'volume': volume,
    'ord_type': 'market',
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
    print(res.text)
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

def get_my_KRW():
    m = hashlib.sha512()


    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(server_url + "/v1/accounts", headers=headers)
    print(float(res.json()[0]["balance"]))
    return float(res.json()[0]["balance"])
    
for j in range(0,len(code)):
    buyflag.append(True)

buymoney = 0 
nowcode = ''
sonik = 0
flag = False
while True:
    if(flag == False):
        for i in range(0,len(code)):
            url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/3?code=CRIX.UPBIT.KRW-"+code[i]+"&count=400"
            response = requests.request("GET", url)
            data = response.json()
            df = pd.DataFrame(data)
            now = time.localtime()
            #print(df.iloc[0]["tradePrice"])
            if(df.iloc[0]["highPrice"] > df.iloc[1]["highPrice"] and df.iloc[0]["tradePrice"] <  df.iloc[1]["highPrice"] and df.iloc[2]["tradePrice"] >  df.iloc[1]["tradePrice"] and df.iloc[3]["tradePrice"] >  df.iloc[2]["tradePrice"] ):
                print(code[i],df.iloc[0]["tradePrice"],"구매")
                ret = upbit.buy_limit_order("KRW-"+code[i], df.iloc[0]["tradePrice"], (get_my_KRW()-300)/df.iloc[0]["tradePrice"])
                print(ret)
                try:
                    cancelcode =ret['uuid']
                    time.sleep(3)
                    ret = upbit.cancel_order(cancelcode)
                    try:
                        if(ret["error"]):
                            nowcode = code[i]
                            flag = True
                            time.sleep(5)
                            break
                    except:
                        pass
                except:
                    pass
                #bot.sendMessa ge(chat_id = '1780594186', text="["+code[j]+"] 구매시도")
                
                
            time.sleep(1)
    else:
        mybal,my_avg_price = get_my_value(nowcode)
        url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/3?code=CRIX.UPBIT.KRW-"+nowcode+"&count=1"
        response = requests.request("GET", url)
        data = response.json()
        if(mybal!=0):
            if(my_avg_price * 1.006 <= data[0]["tradePrice"]):
                #sell(nowcode,mybal,mybal)
                print(nowcode,data[0]["tradePrice"],"판매")
                ret = upbit.sell_limit_order("KRW-"+nowcode, data[0]["tradePrice"], mybal)
                print(ret)
                try:
                    cancelcode =ret['uuid']
                    time.sleep(1)
                    ret = upbit.cancel_order(cancelcode)
                    try:
                        if(ret["error"]):
                            flag = False
                            bot.sendMessage(chat_id = '1780594186', text="["+get_my_KRW()+"]")
                            time.sleep(10)
                    except:
                        time.sleep(0.1)
                except:
                    pass
                

            if(my_avg_price * 0.994  >= data[0]["tradePrice"]):
                #sell(nowcode,mybal,mybal)
                print(nowcode,data[0]["tradePrice"],"판매")
                ret = upbit.sell_limit_order("KRW-"+nowcode, data[0]["tradePrice"], mybal)
                print(ret)
                try:
                    cancelcode =ret['uuid']
                    time.sleep(1)
                    ret = upbit.cancel_order(cancelcode)
                    try:
                        if(ret["error"]):
                            flag = False
                            bot.sendMessage(chat_id = '1780594186', text="["+get_my_KRW()+"]")
                            time.sleep(10)
                            
                    except:
                        time.sleep(0.1)
                except:
                    pass
            if(mybal==0):
                flag = False
        else:
            time.sleep(1)
        time.sleep(0.2)