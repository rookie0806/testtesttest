import requests
import pandas as pd
import time
import webbrowser
#code = ["XRP","DAWN","DOGE","STRK","ETC","SRM","WAVES","BTG","NEO","QTUM","EOS","SC","CBK","PUNDIX","GAS","MLK","SBD","AXS","ONT","OBSR","MVL","FLOW","ARK","MTL","TON","STX","MBL","TSHP","STRAX","ADA","STMX","PCI","CRE","IOST","SXP","DOT","MANA","STEEM","STPT","LINK","QTCON","DMT","RFR","LTC","MFT","LAMB","GRS","EDR","AERGO","BCHA","AQT","BSV","TT","KNC","IQ","QKC","STORJ","ICX","AHT","ZRX","LSK","ONG","XTZ","KAVA","THETA","ENJ","OMG","REP","ATOM","BAT","ADX","IOTA"]
code = ["ADA","MLK","GRS","STX","ZRX","STORJ","IOTA","ARK","ENJ","ONT","ICX","PUNDIX"]#,"KNC","KMD","MTL","STRAX","SXP","AQT","KAVA","DAWN","CBK","XTZ","SBD","AXS","LSK","EOS","SRM","TON","OMG","THETA","GAS","QTUM","FLOW","ATOM","WAVES","DPT","REP","BCHA","LINK","STRK"]
#code = ["BTT","MBL","AHT","TT","MFT","CRE","RFR","TSHP","IQ","MVL","OBSR","QKC","SC","STMX","EDR","IOST","QTCON","LAMB","STPT"]
hap = 0

cnt = 0
plus = 0
topplus = -1000000000
minus = 0
topminus = 100000000
topcoin = ""
topcoinmoney = 0
totalmoney = 2000000
print(len(code))
for j in range(0,len(code)):
    print(code[j])
    try:
        url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/10?code=CRIX.UPBIT.KRW-"+code[j]+"&count=400"

        response = requests.request("GET", url)

        data = response.json()

        df = pd.DataFrame(data)

        df=df.iloc[::-1]
        #print(df)
        buyflag = True
        sonik = 0
        realsonik = 0
        money = 0
        for i in range(4,399):
            #print(df.iloc[i-4]["tradePrice"],df.iloc[i-3]["tradePrice"],df.iloc[i-2]["tradePrice"],df.iloc[i-1]["tradePrice"],df.iloc[i]["tradePrice"])
            if(buyflag):
                if(df.iloc[i]["highPrice"]>df.iloc[i-1]["highPrice"] and df.iloc[i-1]["tradePrice"]<=df.iloc[i-2]["tradePrice"]):
                    buyflag = False
                    price = df.iloc[i-1]["highPrice"]
                    sonik =  totalmoney / price

            if(buyflag == False):
                if(totalmoney/sonik *1.005 <= df.iloc[i]["highPrice"]and buyflag == False):
                    price = totalmoney/sonik *1.005
                    print("구매가격 :",totalmoney/sonik,", 판매가격 :",price,", 이익 :",sonik * price - totalmoney)

                    if(sonik * price - totalmoney >= 0):
                        plus = plus + 1
                        if(topplus<sonik *price - totalmoney):
                            topplus = sonik *price - totalmoney
                    else:
                        minus = minus + 1
                        if(topminus>sonik *price - totalmoney):
                            topminus = sonik *price - totalmoney
                    totalmoney = sonik * price
                    

                    buyflag = True
                    cnt = cnt + 1

                if(df.iloc[i-1]["highPrice"] > df.iloc[i]["highPrice"] and df.iloc[i-1]["lowPrice"] > df.iloc[i]["lowPrice"] and totalmoney/sonik >= df.iloc[i-1]["lowPrice"] and buyflag == False):
                    price = df.iloc[i-1]["lowPrice"]

                    print("구매가격 :",totalmoney/sonik,", 판매가격 :",price,", 이익 :",sonik * price - totalmoney)
                   
                    if(sonik * price - totalmoney >= 0):
                        plus = plus + 1
                        if(topplus<sonik *price - totalmoney):
                            topplus = sonik *price - totalmoney
                    else:
                        minus = minus + 1
                        if(topminus>sonik *price - totalmoney):
                            topminus = sonik *price - totalmoney
                    totalmoney =  sonik * price
                    

                    buyflag = True
                    cnt = cnt + 1
                print(str(totalmoney))
                    #print("sell")
                    #print("sonik",realsonik)
                    #print(df.iloc[i-4]["candleAccTradeVolume"]+df.iloc[i-3]["candleAccTradeVolume"]+df.iloc[i-2]["candleAccTradeVolume"],df.iloc[i-1]["candleAccTradeVolume"],df.iloc[i]["candleAccTradeVolume"]) 
        if(topcoinmoney<money):
            topcoinmoney = money
            topcoin = code[j]
        print(str(totalmoney))
        hap = hap + money
    except Exception as e:
        print("ddddd")
        print(e)
        pass
print("총 이익 : ",hap)
print("구매 횟수 : ",cnt,"평균 구매 횟수 : ",cnt/len(code))
print("이득 횟수 : ",plus,"최고 이득 : ",topplus)
print("손해 횟수 : ",minus,"최고 손해 : ",topminus)
print("탑 코인 :",topcoin,"이익 :",topcoinmoney)
print(hap/400)