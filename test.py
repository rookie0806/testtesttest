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
from pathlib import Path
from sklearn import preprocessing
from keras.models import load_model
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
    self.input_neurons = 9
    self.output_neurons = 1
    self.hidden_neurons = int(length/7*5)
    self.batch_size = 10
    self.epochs = 10
    self.percentage = 0.7
    self.Model = self.create_model()
 
  # prepare data
  def load_data(self, data, n_prev):
    x, y = [], []
    x2 = data[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    y1 = data[['up']]
    
    x1 = x_scale.fit_transform(x2)
    
    x2 = pandas.DataFrame(x1,columns=x2.columns, index=list(x2.index.values))
    y_t = y_scale.fit_transform(y1)
    y2 = pandas.DataFrame(y_t,columns=y1.columns, index=list(y1.index.values))
   
    for i in range(len(data) - n_prev):
        x.append(x2[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']].iloc[i:(i+n_prev)].values)
        y.append(y2.iloc[i+n_prev].values)
        print("---------------------------")
        print(x_scale.inverse_transform(x2[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']].iloc[i:(i+n_prev)].values))
        print(y_scale.inverse_transform(y2.iloc[i+n_prev].values.reshape(-1, 1)))
        print("---------------------------")
    X = numpy.array(x)
    Y = numpy.array(y)
    return X, Y

 
  # make model
  def create_model(self):
    Model = Sequential()
    Model.add(LSTM(50, activation='relu',input_shape=(self.length_of_sequences, self.input_neurons), return_sequences=True))
    Model.add(LSTM(64, return_sequences=False))
    Model.add(Dense(1))
    Model.compile(loss='mean_squared_error', optimizer='adam')
    return Model
    
 
  # do learning
  def train(self, x_train, y_train, epoch):
    self.Model.fit(x_train, y_train, self.batch_size,epoch)

model1 = "" #
model2 = ""
model3 = ""

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
        ohlc["tradePrice"] = ohlc["tradePrice"]
        delta = ohlc["tradePrice"].diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss
        return pd.Series(100 - (100 / (1 + RS)), name="RSI")

def returndata(prices,length,model,first):
    yahoo = prices[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice','up']]
    
    predict = yahoo[-(length+15):]
    yahoo = yahoo[:-(length+15)]
    #print(predict)
    x_train, y_train = model.load_data(yahoo.iloc[0:int(len(yahoo)*1)], length)
    x = []
    y= []
    tp = []
    x1 = predict[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    y1= predict[['up']]
    print(x1)
    
    x_t = x_scale.fit_transform(x1)
    x2 = pandas.DataFrame(x_t,columns=x1.columns, index=list(x1.index.values))
    y_t = y_scale.fit_transform(y1)
    y2 = pandas.DataFrame(y_t,columns=y1.columns, index=list(y1.index.values))
    #print(x1)
    for i in range(0,16):
        x3 = x2.iloc[i:i+length].values
        y3 = y2.iloc[i+length-1].values
        tpv = x1.iloc[i+length-1:i+length].values[0][3]
        #print(tpv)
        x.append(x3)
        y.append(y3)
        tp.append(tpv)
        #print(x_scale.inverse_transform(x3))
    #print(y)
    x = numpy.array(x)
   
    return x_train,y_train,x,tp

    
def modelpredict(prices,length,model,first):
    yahoo = prices[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    
    predict = yahoo[-(length+1):]
    yahoo = yahoo[:-(length+1)]
    x_train, y_train = model.load_data(yahoo.iloc[0:int(len(yahoo)*1)], length)
    x = []
    y= []
    x1 = predict[['OpeningPrice','highPrice','lowPrice','tradePrice','CandleAccTradeVolume','rsi','macd','exp','candleAccTradePrice']]
    y1= predict[['up']]
    x_t = x_scale.fit_transform(x1)
    x2 = pandas.DataFrame(x_t,columns=x1.columns, index=list(x1.index.values))
    for i in range(0,1):
        x3 = x2.iloc[i:i+length].values
        y2 = y1.iloc[i+length-1:i+length].values[0][0]
        x.append(x3)
        y.append(y2)
    x = numpy.array(x)
    model.train(x_train, y_train,10)
    x_predicted = model.predict(x)
    return x_predicted[-1][1]
    #print(numpy.argmax(x_predicted, axis=-1))
    #print(y)
    #print(coin)
    
    

def start(coin, time, rate,predictflag):
    global first,model1,model2,model3
    if(predictflag==False):
        minutes_units = [time]
        for minutes_unit in minutes_units:
            req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-'+coin+'&count=1000')
            data   = req.json()
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
                    TradePrice = float(data[399-i]["tradePrice"])
                    TradePrice1 = float(data[398-i]["tradePrice"])
                    TradePrice2 = float(data[397-i]["tradePrice"])
                    TradePrice3 = float(data[396-i]["tradePrice"])
                    TradePrice4 = float(data[395-i]["tradePrice"])
                    TradePrice5 = float(data[394-i]["tradePrice"])
                    df4=df3.iloc[i-100:i+1].reset_index(drop = True)
                    nowrsi =  rsi(df4[:i].reset_index(), 14).iloc[-1]
                    exp1 = df4.ewm(span=5, adjust=False).mean()
                    exp2 = df4.ewm(span=12, adjust=False).mean()
                    macd = exp1-exp2
                    exp3 = macd.ewm(span=7, adjust=False).mean()
                    #print(macd)
                    #print('MACD: ',macd[0])
                    #print('Signal: ',exp3[0])
                    

                    test = TradePrice
                    result.append({
                        'OpeningPrice'         : data[399-i]["openingPrice"],
                        'highPrice'            : data[399-i]["highPrice"],
                        'lowPrice'             : data[399-i]["lowPrice"],
                        'tradePrice'           : data[399-i]["tradePrice"],
                        'CandleAccTradeVolume' : data[399-i]["candleAccTradeVolume"],
                        "candleAccTradePrice"  : data[399-i]["candleAccTradePrice"],
                        "rsi" :  nowrsi,
                        "macd" : macd[100],
                        "exp" : exp3[100],
                        "up" : data[398-i]["openingPrice"]
                    })
            prices = pd.DataFrame(result)
            rate = []
            avg = []
            tparray = []
            sumrate = 0.0
            buymoney = 0
            stock = 0
            x_train1,y_train1,x,tp = returndata(prices,5,model1,False)
            x_predicted1 = model1.Model.predict(x)
            x_train2,y_train2,x,tp = returndata(prices,10,model2,False)
            x_predicted2 = model2.Model.predict(x)
            x_train3,y_train3,x,tp = returndata(prices,20,model3,False)
            x_predicted3 = model3.Model.predict(x)
            tparray.append(tp)
            for i in range(0,16):
                rate1 = y_scale.inverse_transform(x_predicted1[i][-1].reshape(-1, 1))[0][0]
                rate2 = y_scale.inverse_transform(x_predicted2[i][-1].reshape(-1, 1))[0][0]
                rate3 = y_scale.inverse_transform(x_predicted3[i][-1].reshape(-1, 1))[0][0]
                rate.append([rate1,rate2,rate3])
                avg.append((rate1+rate2+rate3)/3)
                print(tp[i],rate1,rate2,rate3,(rate1+rate2+rate3)/3)
                if(i>1):
                    if(expect>=tp[i-1] and tp[i]>=tp[i-1]):
                        print("예측성공")
                    if(expect<=tp[i-1] and tp[i]<=tp[i-1]):
                        print("예측성공")
                    else:
                        print("예측실패")
                expect = (rate1+rate2+rate3)/3
                print('---------------------')
                
            '''
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
            '''
    else:
        minutes_units = [time]
        for minutes_unit in minutes_units:
            '''
            Scraping minutes data 
            '''
            req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-'+coin+'&count=1000')
            data   = req.json()
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
                    TradePrice = float(data[399-i]["tradePrice"])
                    TradePrice1 = float(data[398-i]["tradePrice"])
                    TradePrice2 = float(data[397-i]["tradePrice"])
                    TradePrice3 = float(data[396-i]["tradePrice"])
                    TradePrice4 = float(data[395-i]["tradePrice"])
                    TradePrice5 = float(data[394-i]["tradePrice"])
                    df4=df3.iloc[i-100:i+1].reset_index(drop = True)
                    nowrsi =  rsi(df4[:i].reset_index(), 14).iloc[-1]
                    exp1 = df4.ewm(span=5, adjust=False).mean()
                    exp2 = df4.ewm(span=12, adjust=False).mean()
                    macd = exp1-exp2
                    exp3 = macd.ewm(span=7, adjust=False).mean()
                    #print(macd)
                    #print('MACD: ',macd[0])
                    #print('Signal: ',exp3[0])
                    

                    test = TradePrice
                    result.append({
                        'OpeningPrice'         : data[399-i]["openingPrice"],
                        'highPrice'            : data[399-i]["highPrice"],
                        'lowPrice'             : data[399-i]["lowPrice"],
                        'tradePrice'           : data[399-i]["tradePrice"],
                        'CandleAccTradeVolume' : data[399-i]["candleAccTradeVolume"],
                        "candleAccTradePrice"  : data[399-i]["candleAccTradePrice"],
                        "rsi" :  nowrsi,
                        "macd" : macd[100],
                        "exp" : exp3[100],
                        "up" : data[398-i]["openingPrice"],
                    })
            prices = pd.DataFrame(result)
            print(prices)
            rate = []
            sumrate = 0.0
            x_train1,y_train1,x1,tp = returndata(prices,5,model1,False)
            x_train2,y_train2,x2,tp = returndata(prices,10,model2,False)
            x_train3,y_train3,x3,tp = returndata(prices,20,model3,False)

            
            model1.train(x_train1, y_train1,500)
            model2.train(x_train2, y_train2,500)
            model3.train(x_train3, y_train3,500)

            x_predicted = model1.Model.predict(x1)
            rate1 = y_scale.inverse_transform(x_predicted[-1].reshape(-1, 1))[0][0]
            x_predicted = model2.Model.predict(x2)
            rate2 =  y_scale.inverse_transform(x_predicted[-1].reshape(-1, 1))[0][0]
            x_predicted = model3.Model.predict(x3)
            rate3 =  y_scale.inverse_transform(x_predicted[-1].reshape(-1, 1))[0][0]

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
            #model1.Model.save("save_1")
            #model2.Model.save("save_2")
            #model3.Model.save("save_3")

def setting():
    global model1,model2,model3
    my_file = Path("save_1")    # Path는 string을 return하는것 아님.window에서만 사용하능함.
    if my_file.is_file():
        model1 = load_model("save_1")
        model2 = load_model("save_2")
        model3 = load_model("save_3")
        print("load 성공")
    else:
        model1 = Predict(5)
        model2 = Predict(10)
        model3 = Predict(20)
if __name__ == '__main__':
    setting()
    start("XRP", sys.argv[2], sys.argv[3],True)
    #start("ADA", sys.argv[2], sys.argv[3],True)
    #start("MLK", sys.argv[2], sys.argv[3],True)
    #start(sys.argv[1], sys.argv[2], sys.argv[3],True)
    #start("ONT", sys.argv[2], sys.argv[3],True)
    start("XRP", sys.argv[2], sys.argv[3],False)
    
    '''
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
        time.sleep(1)'''