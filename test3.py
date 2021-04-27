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

import pandas 
 
access_key = 'qqbypzZxyAPhKoExBDfi0vQiN5YtlhRXxX7ow52X'
secret_key = 'xDsjdKxzpqWPvFX1iFfl12QNhLym3Kfeb1x1ejYx'
server_url = 'https://api.upbit.com'
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)
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
    if(res.status_code==201):
        #return float(res.json()["price"])
        return 1
    else:
       print(res.json())
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

def start(COIN,MIN):
   flag = True
   money = 0
   while True:
      try:
         time.sleep(2)
         url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/'+str(MIN)+'?code=CRIX.UPBIT.KRW-'+COIN+'&count=400'
         response = requests.request("GET", url)
         data = response.json()
         df = pd.DataFrame(data)
         df=df.iloc[::-1]
         df=df['tradePrice']
         exp1 = df.ewm(span=12, adjust=False).mean()
         exp2 = df.ewm(span=26, adjust=False).mean()
         macd = exp1-exp2
         exp3 = macd.ewm(span=9, adjust=False).mean()
         exp4 = df.ewm(span=5, adjust=False).mean()
         exp5 = df.ewm(span=7, adjust=False).mean()
         exp6 = df.ewm(span=10, adjust=False).mean()
         exp7 = df.ewm(span=3, adjust=False).mean()
         test1=macd[0]-exp3[0]
         test2 = macd[1]-exp3[1]
         test3 =macd[2]-exp3[2]
         lastdf = df[:-1]
         bb_center=numpy.mean(df[len(df)-20:len(df)])
         now = time.localtime()
         if(test1>=test2>=test3 and df[1]>=bb_center and df[0]>=exp5[0] and exp7[0]>=bb_center and test1>test2 and test1>0 and exp7[0]>=exp4[0] and exp4[0]>=exp5[0]):
            if(flag==True):
               bot.sendMessage(chat_id = '1780594186', text="["+COIN+"] 구매 signal,"+str(df[0]))
               money = float(df[0])
               flag = False
               time.sleep(3)
               buy(COIN,50000,50000)
               time.sleep(60)

         if((test2+test3)/2>=test1):
            if(flag==False):
               sonik = df[0]-money     
               bot.sendMessage(chat_id = '1780594186', text="["+COIN+"] 판매 signal,"+str(df[0])+","+str(sonik))
               flag = True
               mybal,my_avg_price = get_my_value(COIN)
               if(mybal!=0.0):
                  sellprice = sell(COIN,mybal,mybal)
               time.sleep(60)

      except Exception as e:
         print(e)


if __name__ == '__main__':
   start(sys.argv[1],sys.argv[2])
      


