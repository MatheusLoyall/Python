import matplotlib.pyplot as plt
import seaborn
import pandas_datareader.data as web
import requests
import pandas as pd
import yfinance as yf
import datetime
from statsmodels import tsa
import ta
import quandl
import json
import requests

## Basic Requests on FinnHub

# home = 'https://finnhub.io/api/v1'
# token = 'bppb07vrh5reoatojnsg'
# dataURL = '/calendar/economic'

# r = requests.get(home + dataURL +'?token=' + token)
# print(r.json())

## Basic Requests on AlphaVantage

home = 'https://www.alphavantage.co/query?'
function = ['TIME_SERIES_DAILY','SYMBOL_SEARCH']
search = ['symbol','keywords']
ticker = 'DI'
token = 'YYLF55FQ7BOLP4JQ'

r = requests.get(home + 'function=' + function[1] + '&' + search[1] + '=' + ticker + '&apikey=' + token)
print(r)


# # Get data from 
# initDate = datetime.date.today() - datetime.timedelta(days = 252)
# endDate = datetime.date.today()
# asset = pd.DataFrame(yf.download("BRL=X",initDate,endDate,auto_adjust = True))

# plt.plot(asset['Close'])
# plt.show()
