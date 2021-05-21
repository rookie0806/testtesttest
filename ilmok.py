import pandas as pd
import datetime
import requests
import pandas as pd
import time
import webbrowser
import telegram
a = 1
code = ["XRP","DAWN","DOGE","STRK","ETC","SRM","WAVES","BTG","NEO","QTUM","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
buy_flag = []
pyungdan = []
sonik = []
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)
for i in range(0,len(code)):
    buy_flag.append(True)
    pyungdan.append(0)
    sonik.append(0)
while True:
    for i in range(0,len(code)):
        try:
            url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-"+code[i]+"&count=400"
            response = requests.request("GET", url) 
            data = response.json()  
            df = pd.DataFrame(data)  
            df=df.iloc[::-1]
            print(code[i],df['tradePrice'].iloc[-1])
            high_prices = df['highPrice']
            close_prices = df['tradePrice']
            low_prices = df['lowPrice']
            dates = df.index
            
            nine_period_high =  df['highPrice'].rolling(window=9).max()
            nine_period_low = df['lowPrice'].rolling(window=9).min()
            df['tenkan_sen'] = (nine_period_high + nine_period_low) /2
            
            period26_high = high_prices.rolling(window=26).max()
            period26_low = low_prices.rolling(window=26).min()
            df['kijun_sen'] = (period26_high + period26_low) / 2
            
            df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
            
            period52_high = high_prices.rolling(window=52).max()
            period52_low = low_prices.rolling(window=52).min()
            df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)
            
            
            df['chikou_span'] = close_prices.shift(-26)
            
            if(buy_flag[i]==True):
                if(df['senkou_span_a'].iloc[-1]>=df['senkou_span_b'].iloc[-1] and df['senkou_span_a'].iloc[-3] > df['tradePrice'].iloc[-3] and df['senkou_span_a'].iloc[-2] <= df['tradePrice'].iloc[-2] and df['senkou_span_a'].iloc[-1] <= df['tradePrice'].iloc[-1]):
                    buy_flag[i] = False
                    pyungdan[i]=df['tradePrice'].iloc[-1]
                    print("buy")
            else:
                if(df['tradePrice'].iloc[-1]<df['lowPrice'].iloc[-2]):
                    print("sell")
                    buy_flag[i] = True
                    sonik[i] = sonik[i] +  df['tradePrice'] - pyungdan[i]
                    bot.sendMessage(chat_id = '1780594186', text="["+code[i]+"] 판매 손익 "+str(df['tradePrice'].iloc[-1] - pyungdan[i]))
            time.sleep(0.7)
        except Exception as e:
            print(e)
            pass
