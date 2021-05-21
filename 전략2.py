import requests
import pandas as pd
import time
import webbrowser
#code = ["BTT","MBL","AHT","TT","MFT","CRE","RFR","TSHP","IQ","MVL","OBSR","QKC","SC","STMX","EDR","IOST","QTCON","LAMB","STPT"]
code = ["BTC","ETH","BCH","LTC","BSV","ETC","BTG","NEO","STRK","LINK","REP","DOT","BCHA","WAVES","ATOM","FLOW","QTUM","SBD","GAS"]

cnt = 0
plus = 0
topplus = -1000000000
minus = 0
topminus = 100000000
topcoin = ""
topcoinmoney = 0
totalmoney = 1000000
sonik = 0
sonhae = 0
print(len(code))
for j in range(0,len(code)):
    print(code[j])
    try:
        url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/3?code=CRIX.UPBIT.KRW-"+code[j]+"&count=400"

        response = requests.request("GET", url)

        data = response.json()

        df = pd.DataFrame(data)

        df=df.iloc[::-1]
        #print(df)
        buyflag = True

        realsonik = 0
        money = 0
        price = 10000000
        for i in range(4,399):
            #print(df.iloc[i-4]["tradePrice"],df.iloc[i-3]["tradePrice"],df.iloc[i-2]["tradePrice"],df.iloc[i-1]["tradePrice"],df.iloc[i]["tradePrice"])
            if(df.iloc[i]["highPrice"] >  df.iloc[i-1]["highPrice"] and df.iloc[i-2]["tradePrice"] >  df.iloc[i-1]["tradePrice"] and df.iloc[i-3]["tradePrice"] >  df.iloc[i-2]["tradePrice"]and buyflag):
                price = df.iloc[i-1]["highPrice"]
                buyflag=False
                #totalmoney =  totalmoney / price * df.iloc[i+1]["openingPrice"]
            elif(price * 1.006 <= df.iloc[i]["highPrice"]and buyflag==False):
                totalmoney =  totalmoney * 1.006
                buyflag= True
                print("이익")
                sonik = sonik + 1
            elif(price * 0.994 >= df.iloc[i]["lowPrice"]and buyflag==False):
                totalmoney =  totalmoney * 0.994
                buyflag= True
                sonhae = sonhae + 1
                print("손해")

                

    except Exception as e:
        print(e)
        pass
print(totalmoney,sonik,sonhae)