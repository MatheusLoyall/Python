import matplotlib.pyplot as plt
import seaborn
import requests
import pandas as pd
import datetime
from statsmodels import tsa
import ta
import json
import requests

## Basic Requests using W16

# ticker = "INDJ20"
# startDate = (datetime.date.today() - datetime.timedelta(days = 252)).isoformat()
# endDate = datetime.date.today().isoformat()

# r = requests.get("https://api-w16.loyall.com.br/futures/" + ticker + "?date=" + reqDate)
# data = r.json()
# print(data)

# r = requests.get("https://api-w16.loyall.com.br/shares/" + ticker + "?Date=" + startDate)
