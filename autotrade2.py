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
'''
ret2 = upbit.buy_limit_order("KRW-XRP", 20 , 50000/20)
ret = upbit.cancel_order(ret2['uuid'])
print(ret)
try:
    if(ret["error"]):
        print("yes")
except:
    print("no")
ret = upbit.cancel_order(ret2['uuid'])
print(ret)
try:
    if(ret["error"]):
        print("yes")
except:
    print("no")
'''

#code = ["XRP","DAWN","DOGE","STRK","ETC","SRM","WAVES","BTG","NEO","QTUM","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
#code = ["ETH","QTUM","BTC","XRP","EOS","BCH","BTT","ADA","LTC","KMD","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
#code = ["BTT","MBL","AHT","TT","MFT","CRE","RFR","TSHP","IQ","MVL","OBSR","QKC","SC","STMX","EDR","IOST","QTCON","LAMB","STPT"]
code = ["ADA","MLK","GRS","STX","ZRX","STORJ","IOTA","ARK","ENJ","ONT","ICX","PUNDIX","KNC","KMD","MTL","STRAX","SXP","AQT","KAVA","DAWN","CBK","XTZ","SBD","AXS","LSK","EOS","SRM","TON","OMG","THETA","GAS","QTUM","FLOW","ATOM","WAVES","REP","BCHA","LINK","STRK"]
cancelcode = []
buyflag = []
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)
hap = 0
money = 20000000
cnt = 0
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
    #print(float(res.json()[0]["balance"]))
    return float(res.json()[0]["balance"])
    

for j in range(0,len(code)):
    buyflag.append(True)
    cancelcode.append("")

while True:
    try:
        for j in range(0,len(code)):
            print(code[j])
            
            url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/10?code=CRIX.UPBIT.KRW-"+code[j]+"&count=400"

            response = requests.request("GET", url)

            data = response.json()

            df = pd.DataFrame(data)
            #print(df.iloc[0]["tradePrice"])
            sonik = 0
            realsonik = 0
            mybal,my_avg_price = get_my_value(code[j])
            #print(code[j])
            if(get_my_KRW()>20000):
                if(buyflag[j]==True):
                    if(df.iloc[0]["highPrice"]>df.iloc[1]["highPrice"] and df.iloc[0]["lowPrice"]>df.iloc[1]["lowPrice"] and df.iloc[1]["tradePrice"]<=df.iloc[2]["tradePrice"] and df.iloc[0]["tradePrice"]<=df.iloc[1]["highPrice"]):
                        #print("buy")
                        buytmpflag = True
                        #print(df.iloc[0]["tradePrice"],get_my_KRW(),get_my_KRW()/df.iloc[0]["tradePrice"])
                        ret = upbit.buy_limit_order("KRW-"+code[j], df.iloc[0]["tradePrice"], (get_my_KRW()-10000)/df.iloc[0]["tradePrice"])
                        print(ret)
                        cancelcode[j] =ret['uuid']
                        #bot.sendMessa ge(chat_id = '1780594186', text="["+code[j]+"] 구매시도")
                        time.sleep(3)
            if(mybal!=0.0):
                if(my_avg_price*1.005<=df.iloc[0]["tradePrice"]):
                    ret = upbit.sell_limit_order("KRW-"+code[j], df.iloc[0]["tradePrice"], mybal)
                    print(ret)
                    cancelcode[j] =ret['uuid']
                    time.sleep(3)
                    #bot.sendMessage(chat_id = '1780594186', text="["+code[j]+"] 판매")
                    buytmpflag = False
                    tmp = df.iloc[0]["tradePrice"]
                if(df.iloc[1]["highPrice"] > df.iloc[0]["highPrice"] and df.iloc[1]["lowPrice"] > df.iloc[0]["lowPrice"] and my_avg_price >= df.iloc[1]["lowPrice"]):
                    ret = upbit.sell_limit_order("KRW-"+code[j], df.iloc[0]["tradePrice"], mybal)
                    print(ret)
                    cancelcode[j] =ret['uuid']
                    time.sleep(3)
                    #bot.sendMessage(chat_id = '1780594186', text="["+code[j]+"] 판매")
                    buytmpflag = False
                    tmp = df.iloc[0]["tradePrice"]
            
            if(cancelcode[j]!=""):
                ret = upbit.cancel_order(cancelcode[j])
                try:
                    if(ret["error"]):
                        if(buytmpflag == True):
                            #print(code[j] + "구매 완료")
                            buyflag[j]==False
                            cancelcode[j] = ""
                        else:
                            #print(code[j] + "판매 완료")
                            buyflag[j]==True
                            sonikmoney = (tmp - my_avg_price) * mybal
                            bot.sendMessage(chat_id = '1780594186', text="["+code[j]+"] 손익 : "+ str(sonikmoney))
                            cancelcode[j] = ""
                except:
                    cancelcode[j] = ""
                    '''
                    if(buytmpflag == True):
                        print("구매 실패")
                    else:
                        print("판매 실패")
                    '''
                    pass

            time.sleep(0.1)
    except Exception as e:
            print("에러")
            print(e)
            time.sleep(0.2)
