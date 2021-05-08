import requests
import pandas as pd
import time
import webbrowser

url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/5?code=CRIX.UPBIT.KRW-KMD&count=100"

response = requests.request("GET", url)

data = response.json()

df = pd.DataFrame(data)

df=df.iloc[::-1]

df=df['tradePrice']
print(df)

exp1 = df.ewm(span=5, adjust=False).mean()
exp2 = df.ewm(span=12, adjust=False).mean()
macd = exp1-exp2
exp3 = macd.ewm(span=7, adjust=False).mean()
print(macd)
print('MACD: ',macd[0])

