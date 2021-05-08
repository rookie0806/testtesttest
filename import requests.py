import requests
import pandas as pd
import time
import webbrowser

url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/5?code=CRIX.UPBIT.KRW-KMD&count=400"

response = requests.request("GET", url)

data = response.json()

df = pd.DataFrame(data)

df=df.iloc[::-1]
print(df)

