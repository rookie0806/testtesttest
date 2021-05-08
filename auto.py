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
flag = True
buymoney = 0

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


def autotrading(MIN,COIN):
    global buymoney
    url = 'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/'+str(MIN)+'?code=CRIX.UPBIT.KRW-'+COIN+'&count=400'
    
    response = requests.request("GET", url)
    
    data = response.json()
    
    df = pd.DataFrame(data)

    df=df.reindex(index=df.index[::-1]).reset_index()
    df2=df.reindex(index=df.index[::-1]).reset_index()
    df['close']=df["tradePrice"]
    trade_price = float(df["tradePrice"][199])
    money = 3000000
    number = 0
    rate = 10
    price = 0
    diff = 0
    flag = 0
    sellprice = 0
    buycoin = 0
    sonik = 3000000
    buyflag = False
    highPrice = 0
    lastmsi = 100
    rate = 0.4
    repeat = 1
    for i, candle in enumerate(data):
        if(i>=101):
            rsi_now =  rsi(df[:i+1].reset_index(), 14).iloc[-1]
            rsi_last1 =  rsi(df[:i+1].reset_index(), 14).iloc[-2]
            rsi_last2 =  rsi(df[:i+1].reset_index(), 14).iloc[-3]
            if(rsi_now>=36 and rsi_now>=rsi_last2 and rsi_last1<36):
                if(repeat==1):
                    now_buy = 100000/data[399-i]["tradePrice"]
                else:
                    now_buy = 100000/data[399-i]["tradePrice"] * (1 + 60*(pyungdan-data[399-i]["tradePrice"])/(pyungdan+data[399-i]["tradePrice"])/2)
                number = number + now_buy
                buycoin = buycoin + data[399-i]["tradePrice"]  * now_buy
                sonik = sonik - data[399-i]["tradePrice"]  * now_buy
                pyungdan = buycoin/number
                print(i,"번째 구매 가격 : ",data[399-i]["tradePrice"])
                print("구매 개수 : ", now_buy)
                print("구매 won : ", data[399-i]["tradePrice"]  * now_buy)
                print("남은 돈 : ", sonik)
                print("평단 : ",buycoin/number)
                
                repeat = repeat + 1
            if(rsi_now>=65 and rsi_now<=rsi_last2  and number!=0.0):
                print(i,"번째 판매 가격 : ",data[399-i]["tradePrice"])
                sonik = sonik + data[399-i]["tradePrice"] * number
                print("남은 돈 : ", sonik)
                number = 0
                buycoin = 0
                repeat = 1
        #print("-------------------------")
        '''
        openingPrice = df.iloc[i]["openingPrice"]
        tradePrice = df.iloc[i]["tradePrice"]
        lowPrice = df.iloc[i]["lowPrice"]
        highPrice = df.iloc[i]["highPrice"]
        print("openingPrice : ",openingPrice)
        print("tradePrice : ",tradePrice)
        print("highPrice : ",highPrice)
        print("lowPrice : ",lowPrice)

        if(price==0):
            if(openingPrice>tradePrice ):
                diff = (highPrice-tradePrice)
                price = highPrice - diff*3
                flag = 1
                print(flag,"차 매수 가격 설정완료 : ",price)
                buyflag = False
        else:
            if(highPrice<=price):
                price = highPrice-diff
            if(lowPrice<=price):
                number = number + rate* (1+(flag*0.5))
                money = money - price * rate* (1+(flag*0.5))
                buycoin = buycoin + price * rate* (1+(flag*0.5))
                print(flag,"차 매수 완료 매수 개수 : ",number)
                price = price - diff
                flag = flag + 1
                print(flag,"차 매수 가격 설정완료 : ",price)
                buyflag = True
            if(highPrice>=sellprice and sellprice!=0):
                money = money + sellprice*number
                number = 0
                buyflag = False
                sellprice = 0
                price = 0
                buycoin = 0
                print("매도 완료")
            if(openingPrice<tradePrice):
                if(buyflag==True):
                    if(sellprice==0):
                        sellprice = lowPrice + (tradePrice-lowPrice)*2
                        print("매도 가격 설정완료 : ",sellprice)
                else:
                    print("매수 포인트 초기화")
                    flag = 0
                    price = 0
        calc = money + tradePrice*number
        if(number!=0):
            pyungdan = buycoin/number
        else:
            pyungdan = 0
        print("money : ",money)      
        print("매도 설정 가격 : ",sellprice)  
        print("평단 : ",pyungdan) 
        print("평가 money : ",calc)       
        #c = readchar.readchar()
        

    #print(df)

    df=df.iloc[::-1]
    
    df=df['tradePrice']

    exp1 = df.ewm(span=3, adjust=False).mean()
    exp2 = df.ewm(span=5, adjust=False).mean()
    
    if(flag==True):
        if(exp1[1]<exp2[1] and exp1[0]>=exp2[0] and exp1[0]-exp1[2]>0 and exp1[0]-exp1[1]>0 and exp2[0]-exp2[2]>0 and exp2[0]-exp2[1]>0):
            #buy(COIN,10000,10000)
            bot.sendMessage(chat_id = '1780594186', text="["+COIN+"] 구매 가격 : "+str(df[0]))
            buymoney = int(df[0])
            flag = False
    else:
        if(exp1[1]-exp1[2]>0 and exp1[0]-exp1[1]<0):
            if(abs(exp1[1]-exp1[2])<=abs(exp1[0]-exp1[1])):
                mybal,my_avg_price = get_my_value(COIN)
                #if(mybal!=0.0):
                    #sell(COIN,mybal,mybal)
                bot.sendMessage(chat_id = '1780594186', text="["+COIN+"] 판매 가격 : "+str(df[0])+", 수익 : "+str(df[0]-buymoney))
                flag = True
        elif(exp1[1]-exp1[2]<0 and exp1[0]-exp1[1]<0):
            mybal,my_avg_price = get_my_value(COIN)
            #if(mybal!=0.0):
                #sell(COIN,mybal,mybal)
            bot.sendMessage(chat_id = '1780594186', text="["+COIN+"] 판매 가격 : "+str(df[0])+", 수익 : "+str(df[0]-buymoney))
            flag = True
    time.sleep(5)
    '''
if __name__ == '__main__':
    autotrading(sys.argv[1], sys.argv[2])
    '''
    while True:
        now = time.localtime()
        if(now.tm_min%int(sys.argv[1])==int(sys.argv[1])-1 and now.tm_sec>=54):
            autotrading(sys.argv[1], sys.argv[2])
        time.sleep(1)'''