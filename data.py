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
def rsi(ohlc: pd.DataFrame, period: int = 14):
        ohlc["tradePrice"] = ohlc["tradePrice"]
        delta = ohlc["tradePrice"].diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")
req = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/5?code=CRIX.UPBIT.KRW-KMD&count=1000')
data   = req.json()
#print(data)
df = pd.DataFrame(reversed(data))
df2 = pd.DataFrame(data)
df3 = df2.iloc[::-1]
df3=df3['tradePrice']

df=df.reindex(index=df.index[::-1]).reset_index()
df['close']=df["tradePrice"]
trade_price = float(df["tradePrice"][199])
result = []
test = -100000
up = 0
for i, candle in enumerate(data):
    if(i>=100):
        print('---------------',i-100,i)
        TradePrice = float(data[399-i]["tradePrice"])
        TradePrice1 = float(data[398-i]["tradePrice"])
        TradePrice2 = float(data[397-i]["tradePrice"])
        TradePrice3 = float(data[396-i]["tradePrice"])
        TradePrice4 = float(data[395-i]["tradePrice"])
        TradePrice5 = float(data[394-i]["tradePrice"])
        df4=df3.iloc[i-100:i+1].reset_index(drop = True)
        print(df4)
        nowrsi =  rsi(df4[:i].reset_index(), 14).iloc[-1]
        exp1 = df4.ewm(span=5, adjust=False).mean()
        exp2 = df4.ewm(span=12, adjust=False).mean()
        macd = exp1-exp2
        exp3 = macd.ewm(span=7, adjust=False).mean()
        #print(macd)
        #print('MACD: ',macd[0])
        #print('Signal: ',exp3[0])
        
        if(TradePrice<(TradePrice1+TradePrice2+TradePrice3+TradePrice4+TradePrice5)/5):
            up = 1
        else:
            up = 0
        test = TradePrice
        result.append({
            'OpeningPrice'         : data[399-i]["openingPrice"],
            'HighPrice'            : data[399-i]["highPrice"],
            'LowPrice'             : data[399-i]["lowPrice"],
            'TradePrice'           : data[399-i]["tradePrice"],
            'CandleAccTradeVolume' : data[399-i]["candleAccTradeVolume"],
            "candleAccTradePrice"  : data[399-i]["candleAccTradePrice"],
            "rsi" :  nowrsi,
            "macd" : macd[100],
            "exp" : exp3[100],
            "up" : up
        })
prices = pd.DataFrame(reversed(result))

print(prices)