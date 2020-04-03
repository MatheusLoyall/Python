import matplotlib.pyplot as plt
import seaborn
import requests
import pandas as pd
import datetime
from statsmodels import tsa
import ta
import json
import requests

##  ======== Basic Requests using W16 ========

# === W16 Request essentials ===
auth_token='28dok8hqu9bx'
hed = {'Authorization': 'bearer ' + auth_token}
url = "https://api-w16.loyall.com.br/futures/"
complement = "/history"

# === Parameters ===
ticker = "INDJ20"
startDate = (datetime.date.today() - datetime.timedelta(days = 252)).isoformat()

# === Request ===
r = requests.get(url + ticker + complement, headers = hed)

# === Output ===

writer = pd.ExcelWriter("C:/Users/mpires/Desktop/test.xlsx")

data = pd.DataFrame(r.json()['history'])
data = data.set_index('createdAt')

data.to_excel(writer)
writer.save()

## ===========================================
