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

# W16 Request essentials
auth_token='28dok860e9kb'
hed = {'Authorization': 'Bearer ' + auth_token}
url = "https://api-w16.loyall.com.br/futures/"
complement = "/history"

# Asset essentials
ticker = "INDJ20"

# Dates
startDate = (datetime.date.today() - datetime.timedelta(days = 252)).isoformat()

# The request
r = requests.get(url + ticker + complement, headers = hed)

# The Output
data = pd.DataFrame(r.json()['history'])
data = data.set_index('updatedAt')
print(data.to_excel)


