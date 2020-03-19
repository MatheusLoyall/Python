import matplotlib.pyplot as plt
import seaborn
import pandas_datareader.data as web
import requests
import pandas as pd
import yfinance as yf
import datetime
from statsmodels import tsa
import requests_cache
import ta
import quandl
import json
import requests


## Basic Requests using YahooFinance
 
initDate = datetime.date.today() - datetime.timedelta(days = 252)
endDate = datetime.date.today()

## Mode #1 - yFinance

# f = pd.DataFrame(yf.download("BRL=X",initDate,endDate,auto_adjust = True))

## Mode #2 - Pandas-Datareader

expire_after = datetime.timedelta(days=3)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
f = web.DataReader("URTH", 'yahoo', initDate, endDate, session=session)

plt.plot(f['Close'])
plt.show()
