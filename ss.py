import pandas as pd
from keras.layers.core import Dense, Dropout
from keras.layers.recurrent import GRU
from keras.models import Sequential, load_model
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
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
x_scale = MinMaxScaler()
y_scale = MinMaxScaler()

model_name = 'stock_price_GRU'

model = Sequential()
model.add(GRU(units=50,
            return_sequences=True,
            input_shape=(1, 6)))
model.add(Dropout(0.15))
model.add(GRU(units=50))
model.add(Dropout(0.15))
model.add(Dense(1, activation='tanh'))
model.compile(loss='mse', optimizer='adam')

access_key = 'qqbypzZxyAPhKoExBDfi0vQiN5YtlhRXxX7ow52X'
secret_key = 'xDsjdKxzpqWPvFX1iFfl12QNhLym3Kfeb1x1ejYx'
server_url = 'https://api.upbit.com'
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)
first = True
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
        return float(res.json()["price"])
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

def start(coin, time, rate):
    print(coin,time)
    minutes_units = [time]
    for minutes_unit in minutes_units:
        '''
        Scraping minutes data 
        '''
        req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-'+coin+'&count=1000')
        data   = req.json()
        #print(data)
        df = pd.DataFrame(reversed(data))
        df2 = pd.DataFrame(data)
        
        df=df.reindex(index=df.index[::-1]).reset_index()
        df['close']=df["tradePrice"]
        trade_price = float(df["tradePrice"][199])
        result = []
        test = -100000
        up = 0
        for i, candle in enumerate(data):
            if(i>=100):
                TradePrice = float(data[399-i]["tradePrice"])
                nowrsi =  rsi(df[:i].reset_index(), 14).iloc[-1]
                df3=df2.iloc[i-100:i]['tradePrice'].reset_index(drop = True).iloc[::-1]

                exp1 = df3.ewm(span=12, adjust=False).mean()
                exp2 = df3.ewm(span=26, adjust=False).mean()
                macd = exp1-exp2
                exp3 = macd.ewm(span=9, adjust=False).mean()
                
                #print('MACD: ',macd[0])
                #print('Signal: ',exp3[0])
                
                if(TradePrice*(1+0.01*float(rate))<test):
                    up = up+1
                else:
                    if(TradePrice>=test):
                        up = 0
                    else:
                        pass
                test = TradePrice
                result.append({
                    'OpeningPrice'         : data[399-i]["openingPrice"],
                    'HighPrice'            : data[399-i]["highPrice"],
                    'LowPrice'             : data[399-i]["lowPrice"],
                    'TradePrice'           : data[399-i]["tradePrice"],
                    'CandleAccTradeVolume' : data[399-i]["candleAccTradeVolume"],
                    "candleAccTradePrice"  : data[399-i]["candleAccTradePrice"],
                    "rsi" :  nowrsi,
                    "macd" : macd[0],
                    "exp" : exp3[0],
                    "up" : up
                })
        prices = pd.DataFrame(result)