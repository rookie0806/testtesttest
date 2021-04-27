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
from bs4 import BeautifulSoup

def start(coin, time, rate):
    print(coin,time)
    minutes_units = [time]
    for minutes_unit in minutes_units:
        '''
        Scraping minutes data 
        '''
        req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-'+coin+'&count=1000')
        data   = req.json()
        result = []
        test = 1000000
        for i, candle in enumerate(data):
            TradePrice = float(data[i]["tradePrice"])
            if(TradePrice<test*(1-0.01*float(rate))):
                up = 1
            else:
                up = 0
            test = TradePrice
            result.append({
                'Time'                 : data[i]["candleDateTimeKst"], 
                'OpeningPrice'         : data[i]["openingPrice"],
                'HighPrice'            : data[i]["highPrice"],
                'LowPrice'             : data[i]["lowPrice"],
                'TradePrice'           : data[i]["tradePrice"],
                'CandleAccTradeVolume' : data[i]["candleAccTradeVolume"],
                "candleAccTradePrice"  : data[i]["candleAccTradePrice"],
                "up" : up
            })
        coin_data = pd.DataFrame(reversed(result))
        prices = coin_data.set_index('Time')
        yahoo = prices[:-1]

        yahoo = yahoo[['OpeningPrice', 'LowPrice', 'HighPrice', 'TradePrice','CandleAccTradeVolume','candleAccTradePrice','up']]

        predict = yahoo[-10:]
        yahoo = yahoo[:-10]
        print(predict)
        # preparing label data
        #yahoo_shift = yahoo.shift(-1)
        label = yahoo['up']

        # adjusting the shape of both
        yahoo.drop(yahoo.index[len(yahoo)-1], axis=0, inplace=True)
        label.drop(label.index[len(label)-1], axis=0, inplace=True)

        # conversion to numpy array
        x, y = yahoo.values, label.values


        # scaling values for model
        x_scale = MinMaxScaler()
        y_scale = MinMaxScaler()

        X = x_scale.fit_transform(x)
        test = x_scale.fit_transform(predict)
        Y = y_scale.fit_transform(y.reshape(-1,1))

        # splitting train and test
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
        X_train = X_train.reshape((-1,1,7))
        X_test = X_test.reshape((-1,1,7))
        test = test.reshape((-1,1,7))
        # creating model using Keras
        # tf.reset_default_graph()

        model_name = 'stock_price_GRU'

        model = Sequential()
        model.add(GRU(units=50,
                    return_sequences=True,
                    input_shape=(1, 7)))
        model.add(Dropout(0.2))
        model.add(GRU(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='hard_sigmoid'))
        model.compile(loss='mse', optimizer='adam')

        # model = load_model("{}.h5".format(model_name))
        # print("MODEL-LOADED")

        model.fit(X_train,y_train,batch_size=1024, epochs=2500, validation_split=0.1, verbose=1)
        model.save("{}.h5".format(model_name))
        print('MODEL-SAVED')

        score = model.evaluate(X_test, y_test, batch_size=1024)
        print('Score: ',score)
        yhat = model.predict(X_test)
        print(predict)
        yhat = y_scale.inverse_transform(yhat)
        test = model.predict(test)
        ztest = y_scale.inverse_transform(test)
        print(ztest)
        y_test = y_scale.inverse_transform(y_test)

if __name__ == '__main__':
    start(sys.argv[1], sys.argv[2],sys.argv[3])