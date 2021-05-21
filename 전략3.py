import pandas as pd
import datetime
import requests
import pandas as pd
import time
import webbrowser
import telegram
import math
a = 1
code = ["AXS"]#,"DAWN","DOGE","STRK","ETC","SRM","WAVES","BTG","NEO","QTUM","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
buy_flag = []
pyungdan = []
sonik = []
telegram_token = '1787639638:AAEN5XFWnceuxvs7qWQxMkQGdxHgzdisHb4'
bot = telegram.Bot(token = telegram_token)
url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.KRW-"+code[0]+"&count=400"
response = requests.request("GET", url) 
data = response.json()  
df = pd.DataFrame(data)  
df = df.iloc[::-1].reset_index(drop=True)
high_prices = df['highPrice']
close_prices = df['tradePrice']
low_prices = df['lowPrice']
opening_prices = df['openingPrice']
dates = df.index

print(high_prices)
money = 1000000
for i in range(1,400):
    if(high_prices[i]>=high_prices[i-1]-low_prices[i-1]+opening_prices[i]):
        if(high_prices[i]>=(high_prices[i-1]-low_prices[i-1]+opening_prices[i])*1.02):
            money = money * 1.02
            print("2퍼센트 익절")
            print(money)
        else:
            if((close_prices[i]-(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))/(high_prices[i-1]-low_prices[i-1]+opening_prices[i])<=0):
                print("close 손절",(close_prices[i]-(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))/(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))
            else:
                print("close 익절",(close_prices[i]-(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))/(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))
            money = money * (1 + (close_prices[i]-(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))/(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))
            print(money)
            #print((close_prices[i]-(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))/(high_prices[i-1]-low_prices[i-1]+opening_prices[i]))
            
    