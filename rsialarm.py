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

symbols = ["XRP","DAWN","BTT","DOGE","STRK","VET","BTC","HIVE","ETC","SRM","ETH","WAVES","MED","BTG","CHZ","NEO","QTUM","EOS","SC","CBK","PUNDIX","MARO","GAS","ZIL","MLK","SBD","PXL","AXS","OBSR","BCH","XEM","TRX","MVL","MOC","FLOW","DKA","ARK","MTL","TON","META","STX","SNT","MBL","XLM","TSHP","PLA","EMC2","STRAX","ADA","STMX","KMD","ORBS","PCI","CRE","IOST","SXP","MANA","STEEM","STPT","SSX","LINK","QTCON","DMT","RFR","ONT","CRO","BORA","LTC","MFT","LAMB","GRS","EDR","FCT2","AERGO","BCHA","AQT","DOT","BSV","UPP","TT","KNC","IQ","HUM","POWR","QKC","TFUEL","STORJ","HUNT","ICX","AHT","ARDR","JST","ZRX","WAXP","LSK","ONG","XTZ","KAVA","THETA","ANKR","HBAR","ENJ","OMG","REP","SAND","LBC","POLY","IGNIS","SOLVE","LOOM","CVC","GLM","ELF","ATOM","BAT","ADX","IOTA"]
buycoin = []
number = []
repeat = []
pyungdan = []
rsi_lasts = []
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
            price = df["trade_price"].iloc[-1]
            if(rsi_lasts[i]!=rsi_last):
                if(rsi_now>=35 and rsi_last<35):
                    if(repeat[i]==1):
                        now_buy = 50000/price
                    else:
                        now_buy = 50000/price * (1 + 30*(pyungdan[i]-price)/(pyungdan[i]+price)/2)
                    number[i] = number[i] + now_buy
                    buycoin[i] = buycoin[i] + price  * now_buy
                    pyungdan[i] = buycoin[i]/number[i]
                    bot.sendMessage(chat_id = '1780594186', text="["+symbols[i]+"] 구매("+str(repeat[i])+") 신호 "+str(price )+"원, 총 구매 :"+str(price* now_buy))
                    repeat[i] = repeat[i] + 1
                if(rsi_now>=65 and number[i]!=0):
                    bot.sendMessage(chat_id = '1780594186', text="["+symbols[i]+"] 판매 신호(65) "+str(price)+"원")
                    number[i] = 0
                    buycoin[i] = 0
                    repeat[i] = 1
                rsi_lasts[i] = rsi_last
        except Exception as e:
            print(e)
            time.sleep(1)