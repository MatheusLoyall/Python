from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import yfinance as yf
import datetime
import talib as ta
import pandas_datareader.data as web


initDate = datetime.date.today() - datetime.timedelta(days = 252)

endDate = datetime.date.today()

asset = yf.download('BRL=X',start = initDate, end = endDate)








# plot_acf(asset['Close'], lags=20)
# pyplot.show()

# plot_pacf(asset['Close'], lags=20)
# pyplot.show()
