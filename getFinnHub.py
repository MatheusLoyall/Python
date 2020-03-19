import matplotlib.pyplot as plt
import seaborn
import requests
import pandas as pd
import datetime
from statsmodels import tsa
import ta
import json
import requests

## Basic Requests using FinnHub

home = 'https://finnhub.io/api/v1'
token = 'bppb07vrh5reoatojnsg'
dataURL = '/calendar/economic'

r = requests.get(home + dataURL +'?token=' + token)
print(r.json())
