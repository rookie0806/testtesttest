import requests
import pandas as pd
import time
import webbrowser
code = ["XRP","DAWN","DOGE","STRK","ETC","SRM"]#,"WAVES","BTG","NEO","QTUM","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
hap = 0

cnt = 0
plus = 0
topplus = -1000000000
minus = 0
topminus = 100000000
topcoin = ""
topcoinmoney = 0
money = 2000000
print(len(code))
for j in range(0,len(code)):
    print(code[j])
    try:
        url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.KRW-"+code[j]+"&count=400"

        response = requests.request("GET", url)

        data = response.json()

        df = pd.DataFrame(data)

        df=df.iloc[::-1]
        #print(df)
        buyflag = True
        sonik = 0
        realsonik = 0
        for i in range(4,399):
            #print(df.iloc[i-4]["tradePrice"],df.iloc[i-3]["tradePrice"],df.iloc[i-2]["tradePrice"],df.iloc[i-1]["tradePrice"])
            if(buyflag):
                if(df.iloc[i]["highPrice"]>df.iloc[i-1]["highPrice"] and df.iloc[i-1]["tradePrice"]<=df.iloc[i-2]["tradePrice"] and df.iloc[i]["highPrice"]>df.iloc[i-2]["highPrice"] ):
                    buyflag = False
                    price = df.iloc[i-1]["highPrice"]
                    if(price<=100):
                        price = price+0.2
                    elif(price<=1000):
                        price = price+2
                    elif(price<=10000):
                        price = price+10
                    elif(price<=100000):
                        price = price+20
                    elif(price<=1000000):
                        price = price+100
                    sonik =  money / price
            else:
                

                if(df.iloc[i-1]["lowPrice"]>df.iloc[i]["tradePrice"] and buyflag == False):
                    price = df.iloc[i-1]["lowPrice"]
                    if(price<=100):
                        price = price-0.2
                    elif(price<=1000):
                        price = price-2
                    elif(price<=10000):
                        price = price-10
                    elif(price<=100000):
                        price = price-20
                    elif(price<=1000000):
                        price = price-100
                    print("???????????? :",money/sonik,", ???????????? :",price,", ?????? :",sonik * price - money)
                   
                    if(sonik * price - money >= 0):
                        plus = plus + 1
                        if(topplus<sonik *price - money):
                            topplus = sonik *price - money
                    else:
                        minus = minus + 1
                        if(topminus>sonik *price - money):
                            topminus = sonik *price - money
                    money =  money + sonik * price - money
                    print("?????? ??? :", money)
                    buyflag = True
                    cnt = cnt + 1

                    #print("sell")
                    #print("sonik",realsonik)
                    #print(df.iloc[i-4]["candleAccTradeVolume"]+df.iloc[i-3]["candleAccTradeVolume"]+df.iloc[i-2]["candleAccTradeVolume"],df.iloc[i-1]["candleAccTradeVolume"],df.iloc[i]["candleAccTradeVolume"]) 
        if(topcoinmoney<money):
            topcoinmoney = money
            topcoin = code[j]
        print(str(money))
        hap = hap + money
    except:
        pass
print("??? ?????? : ",hap)
print("?????? ?????? : ",cnt,"?????? ?????? ?????? : ",cnt/len(code))
print("?????? ?????? : ",plus,"?????? ?????? : ",topplus)
print("?????? ?????? : ",minus,"?????? ?????? : ",topminus)
print("??? ?????? :",topcoin,"?????? :",topcoinmoney)
print(hap/400)