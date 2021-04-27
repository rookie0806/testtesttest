import requests
import pandas as pd

from bs4 import BeautifulSoup

coin_list       = ['LINK'] 
time_units      = ['days', 'weeks']
minutes_units   = [60, 240] 

'''
'Time'                 : 시간
'OpeningPrice'         : 시가
'HighPrice'            : 고가
'LowPrice'             : 저가
'TradePrice'           : 체결가
'CandleAccTradeVolume' : 누적 거래량
'CandleAccTradePrice'  : 누적 체결가
'''

for coin in coin_list:
    
    for time_unit in time_units:
        '''
        Scraping days & weeks 
        '''
        req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/{time_unit}?code=CRIX.UPBIT.KRW-{coin}&count=100&')
        data   = req.json()
        result = []

        for i, candle in enumerate(data):
            result.append({
                'Time'                 : data[i]["candleDateTimeKst"], 
                'OpeningPrice'         : data[i]["openingPrice"],
                'HighPrice'            : data[i]["highPrice"],
                'LowPrice'             : data[i]["lowPrice"],
                'TradePrice'           : data[i]["tradePrice"],
                'CandleAccTradeVolume' : data[i]["candleAccTradeVolume"],
                "candleAccTradePrice"  : data[i]["candleAccTradePrice"]
            })
        coin_data = pd.DataFrame(result.reverse())
        coin_data.to_csv(f'{coin}_KRW_{time_unit}.csv')


    for minutes_unit in minutes_units:
        '''
        Scraping minutes data 
        '''
        req    = requests.get(f'https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/{minutes_unit}?code=CRIX.UPBIT.KRW-{coin}&count=1000')
        data   = req.json()
        result = []
        test = 1000000
        for i, candle in enumerate(data):
            TradePrice = float(data[i]["tradePrice"])
            if(TradePrice<test*0.995):
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
        coin_data = coin_data.set_index('Time')
        coin_data.to_csv(f'{coin}_KRW_{minutes_unit}min.csv')