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
import numpy
import numpy
from sklearn.preprocessing import OneHotEncoder
import pandas
import matplotlib.pyplot as plt
 
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.layers import LeakyReLU
from keras.losses import binary_crossentropy   
from keras.optimizers import Adam   
 
x_scale = MinMaxScaler()
y_scale = MinMaxScaler()
first = False
class Predict:
  def __init__(self,length):
    self.length_of_sequences = length
    self.input_neurons = 13
    self.output_neurons = 2
    self.hidden_neurons = 300
    self.batch_size = 10
    self.epochs = 10
    self.percentage = 0.8
    self.Model = self.create_model()
 
  # prepare data
  def load_data(self, data, n_prev):
    x, y = [], []
    x2 = data[['openingPrice','highPrice','lowPrice','tradePrcie','bb_center', 'band1', 'stochrsi_D','stochrsi_K','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    y2 = data[['up']]
    x1 = x_scale.fit_transform(x2)
    x2 = pandas.DataFrame(x1,columns=x2.columns, index=list(x2.index.values))

    for i in range(len(data) - n_prev):
        x.append(x2[['openingPrice','highPrice','lowPrice','tradePrcie','bb_center', 'band1', 'stochrsi_D','stochrsi_K','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']].iloc[i:(i+n_prev)].values)
        y.append(y2[['up']].iloc[i+n_prev].values[0])
    X = numpy.array(x)
    Y = numpy.array(y)
    return X, Y
 
  # make model
  def create_model(self):
    Model = Sequential()
    Model.add(LSTM(128, activation='relu',input_shape=(self.length_of_sequences, self.input_neurons), return_sequences=True))
    Model.add(Dropout(0.3))
    Model.add(LSTM(64, return_sequences=False))
    Model.add(Dropout(0.3))
    Model.add(Dense(2, activation='softmax'))

    Model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy']
              )
    return Model
 
  # do learning
  def train(self, x_train, y_train, epoch):
    self.Model.fit(x_train, y_train, self.batch_size,epoch)



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

def returndata(prices,length,model,first):
    yahoo = prices[['openingPrice','highPrice','lowPrice','tradePrcie','bb_center',  'stochrsi_D','stochrsi_K','band1', 'CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice','up']]
    predict = yahoo[-(length+1):]
    yahoo = yahoo[:-(length+1)]
    x_train, y_train = model.load_data(yahoo.iloc[0:int(len(yahoo)*0.7)], length)
    x_test, y_test = model.load_data(yahoo.iloc[int(len(yahoo)*0.7):], length)
    x = []
    y= []
    x1 = predict[['openingPrice','highPrice','lowPrice','tradePrcie','bb_center', 'band1',  'stochrsi_D','stochrsi_K','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    y1= predict[['up']]
    x_t = x_scale.fit_transform(x1)
    x2 = pandas.DataFrame(x_t,columns=x1.columns, index=list(x1.index.values))
    for i in range(0,1):
        x3 = x2.iloc[i:i+length].values
        y2 = y1.iloc[i+length-1:i+length].values[0][0]
        x.append(x3)
        y.append(y2)
    x = numpy.array(x)
    return x_train,y_train,x

    
def modelpredict(prices,length,model,first):
    yahoo = prices[['openingPrice','highPrice','lowPrice','tradePrcie','bb_center',  'stochrsi_D','stochrsi_K','band1', 'CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice','up']]
    predict = yahoo[-(length+1):]
    yahoo = yahoo[:-(length+1)]
    x_train, y_train = model.load_data(yahoo.iloc[0:int(len(yahoo)*1)], length)
    x = []
    y= []
    x1 = predict[['openingPrice','highPrice','lowPrice','tradePrcie','bb_center', 'band1',  'stochrsi_D','stochrsi_K','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    y1= predict[['up']]
    x_t = x_scale.fit_transform(x1)
    x2 = pandas.DataFrame(x_t,columns=x1.columns, index=list(x1.index.values))
    for i in range(0,1):
        x3 = x2.iloc[i:i+length].values
        y2 = y1.iloc[i+length-1:i+length].values[0][0]
        x.append(x3)
        y.append(y2)
    x = numpy.array(x)
    if(first):
        model.train(x_train, y_train,200)
        x_predicted = model.predict(x)
        return x_predicted[-1][1]
    else:
        model.train(x_train, y_train,10)
        x_predicted = model.predict(x)
        return x_predicted[-1][1]
    #print(numpy.argmax(x_predicted, axis=-1))
    #print(y)
    #print(coin)
    
    

def start(coin, time, rate, model1, model2, model3):
    global first
    if(first):
        minutes_units = [time]
        for minutes_unit in minutes_units:
            req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-'+coin+'&count=1000')
            data   = req.json()
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
                    TradePrice1 = float(data[398-i]["tradePrice"])
                    TradePrice2 = float(data[397-i]["tradePrice"])
                    TradePrice3 = float(data[396-i]["tradePrice"])
                    nowrsi =  rsi(df[:i].reset_index(), 14).iloc[-1]
                    df3=df2.iloc[i-100:i]['tradePrice'].reset_index(drop = True).iloc[::-1]
                    exp1 = df3.ewm(span=12, adjust=False).mean()
                    exp2 = df3.ewm(span=26, adjust=False).mean()
                    exp4 = df3.ewm(span=5, adjust=False).mean()
                    exp5 = df3.ewm(span=10, adjust=False).mean()
                    macd = exp1-exp2
                    exp3 = macd.ewm(span=9, adjust=False).mean()
                    bb_center=numpy.mean(df3[len(df3)-20:len(df3)])
                    band1=2*numpy.std(df3[len(df3)-20:len(df3)])
                    period=14
                    smoothK=3
                    smoothD=3 
                    delta = df3.diff().dropna()
                    ups = delta * 0
                    downs = ups.copy()
                    ups[delta > 0] = delta[delta > 0]
                    downs[delta < 0] = -delta[delta < 0]
                    ups[ups.index[period-1]] = np.mean( ups[:period] )
                    ups = ups.drop(ups.index[:(period-1)])
                    downs[downs.index[period-1]] = np.mean( downs[:period] )
                    downs = downs.drop(downs.index[:(period-1)])
                    rs = ups.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() / \
                        downs.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() 
                    rsi2 = 100 - 100 / (1 + rs)
                    stochrsi  = (rsi2 - rsi2.rolling(period).min()) / (rsi2.rolling(period).max() - rsi2.rolling(period).min())
                    stochrsi_K = stochrsi.rolling(smoothK).mean()
                    stochrsi_D = stochrsi_K.rolling(smoothD).mean()
                    stochrsi_K = stochrsi_K.iloc[-1]*100
                    stochrsi_D = stochrsi_D.iloc[-1]*100
                    if(TradePrice<=TradePrice1):
                        up = [0,1]
                    else:
                        up = [1,0]
                    result.append({
                        'openingPrice' : data[399-i]["openingPrice"],
                        'highPrice' : data[399-i]["highPrice"],
                        'lowPrice' : data[399-i]["lowPrice"],
                        'tradePrcie' : data[399-i]["tradePrice"],
                        'bb_center'         : bb_center,
                        'band1'            : band1,
                        'CandleAccTradeVolume' : data[399-i]["candleAccTradePrice"],#-stochrsi_K,#data[399-i]["candleAccTradeVolume"],
                        "candleAccTradePrice"  : data[399-i]["candleAccTradeVolume"],#data[399-i]["candleAccTradePrice"],
                        "rsi" :  nowrsi,
                        "macd" : macd[0],
                        "exp" : exp3[0],
                        "stochrsi_D" :  stochrsi_D,
                        "stochrsi_K" : stochrsi_K,
                        "up" : up,
                    })
            prices = pd.DataFrame(result)
            rate = []
            sumrate = 0.0
            x_train1,y_train1,x = returndata(prices,5,model1,False)
            x_predicted = model1.Model.predict(x)
            rate1 = x_predicted[-1][1]
            x_train2,y_train2,x = returndata(prices,8,model2,False)
            x_predicted = model2.Model.predict(x)
            rate2 = x_predicted[-1][1]
            x_train3,y_train3,x = returndata(prices,11,model3,False)
            x_predicted = model3.Model.predict(x)
            rate3 = x_predicted[-1][1]

            
            rate.append(rate1)
            rate.append(rate2)
            rate.append(rate3)

            sumrate = rate1 + rate2 + rate3
            avg = sumrate/3

            if(avg>=0.66):
                if(buy(coin,50000,50000)):
                    mybal,my_avg_price = get_my_value(coin)
                    bot.sendMessage(chat_id = '1780594186', text="["+coin+"] ["+str(time)+"] 코인 구매 완료 상승 신뢰도 "+str(float(round(x_predicted[-1][1],2)*100)))
                else:
                    bot.sendMessage(chat_id = '1780594186', text="["+coin+"] 코인 구매 실패 확인 바람")
            if(avg<0.5):
                mybal,my_avg_price = get_my_value(coin)
                if(mybal!=0.0):
                    sellprice = sell(coin,mybal,trade_price)
                else:
                    sellprice = 0
                if(sellprice!=0):
                    bot.sendMessage(chat_id = '1780594186', text="["+coin+"] ["+str(time)+"] 코인 판매 완료")
                else:
                    if(mybal!=0.0):
                        bot.sendMessage(chat_id = '1780594186', text="["+coin+"] 코인 판매 실패 확인 바람")
            
            model1.train(x_train1, y_train1,100)
            model2.train(x_train2, y_train2,100)
            model3.train(x_train3, y_train3,100)

            print(coin)
            print(rate)
            print(avg)
    else:
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
                    TradePrice1 = float(data[398-i]["tradePrice"])
                    TradePrice2 = float(data[397-i]["tradePrice"])
                    TradePrice3 = float(data[396-i]["tradePrice"])
                    nowrsi =  rsi(df[:i].reset_index(), 14).iloc[-1]
                    df3=df2.iloc[i-100:i]['tradePrice'].reset_index(drop = True).iloc[::-1]

                    exp1 = df3.ewm(span=12, adjust=False).mean()
                    exp2 = df3.ewm(span=26, adjust=False).mean()
                    exp4 = df3.ewm(span=5, adjust=False).mean()
                    exp5 = df3.ewm(span=10, adjust=False).mean()
                    macd = exp1-exp2
                    exp3 = macd.ewm(span=9, adjust=False).mean()
                    bb_center=numpy.mean(df3[len(df3)-20:len(df3)])
                    band1=2*numpy.std(df3[len(df3)-20:len(df3)])
                    period=14
                    smoothK=3
                    smoothD=3
                    
                    delta = df3.diff().dropna()
                    ups = delta * 0
                    downs = ups.copy()
                    ups[delta > 0] = delta[delta > 0]
                    downs[delta < 0] = -delta[delta < 0]
                    ups[ups.index[period-1]] = np.mean( ups[:period] )
                    ups = ups.drop(ups.index[:(period-1)])
                    downs[downs.index[period-1]] = np.mean( downs[:period] )
                    downs = downs.drop(downs.index[:(period-1)])
                    rs = ups.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() / \
                        downs.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() 
                    rsi2 = 100 - 100 / (1 + rs)

                    stochrsi  = (rsi2 - rsi2.rolling(period).min()) / (rsi2.rolling(period).max() - rsi2.rolling(period).min())
                    stochrsi_K = stochrsi.rolling(smoothK).mean()
                    stochrsi_D = stochrsi_K.rolling(smoothD).mean()
                    stochrsi_K = stochrsi_K.iloc[-1]*100
                    stochrsi_D = stochrsi_D.iloc[-1]*100
    
                    #print('MACD: ',macd[0])
                    #print('Signal: ',exp3[0])
                    if(TradePrice<=TradePrice1):
                        up = [0,1]
                    else:
                        up = [1,0]
                    result.append({
                        'openingPrice' : data[399-i]["openingPrice"],
                        'highPrice' : data[399-i]["highPrice"],
                        'lowPrice' : data[399-i]["lowPrice"],
                        'tradePrcie' : data[399-i]["tradePrice"],
                        'bb_center'         : bb_center,
                        'band1'            : band1,
                        'CandleAccTradeVolume' : data[399-i]["candleAccTradePrice"],#-stochrsi_K,#data[399-i]["candleAccTradeVolume"],
                        "candleAccTradePrice"  : data[399-i]["candleAccTradeVolume"],#data[399-i]["candleAccTradePrice"],
                        "rsi" :  nowrsi,
                        "macd" : macd[0],
                        "exp" : exp3[0],
                        "stochrsi_D" :  stochrsi_D,
                        "stochrsi_K" : stochrsi_K,
                        "up" : up,
                    })
            prices = pd.DataFrame(result)
            rate = []
            sumrate = 0.0
            x_train1,y_train1,x1 = returndata(prices,5,model1,False)
            x_train2,y_train2,x2 = returndata(prices,8,model2,False)
            x_train3,y_train3,x3 = returndata(prices,11,model3,False)

            
            model1.train(x_train1, y_train1,1000)
            model2.train(x_train2, y_train2,1000)
            model3.train(x_train3, y_train3,1000)

            x_predicted = model1.Model.predict(x1)
            rate1 = x_predicted[-1][1]
            x_predicted = model2.Model.predict(x2)
            rate2 = x_predicted[-1][1]
            x_predicted = model3.Model.predict(x3)
            rate3 = x_predicted[-1][1]

            rate = []
            sumrate = 0.0
            rate.append(rate1)
            rate.append(rate2)
            rate.append(rate3)

            sumrate = rate1 + rate2 + rate3 
            avg = sumrate/3
            print(rate)
            print(avg)
            first = True

if __name__ == '__main__':
    predict1 = Predict(5)
    predict2 = Predict(8)
    predict3 = Predict(11)
    flag = True
    while True:
        now = time.localtime()
        if(now.tm_min%int(sys.argv[2])==int(sys.argv[2])-1 and now.tm_sec>=int(sys.argv[4]) and flag == True):
            try:
                start(sys.argv[1], sys.argv[2],sys.argv[3],predict1,predict2,predict3)
            except:
                pass
            flag = False
        if(now.tm_min%int(sys.argv[2])!=int(sys.argv[2])-1):
            flag = True
        time.sleep(1)