from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import yfinance as yf
import datetime

asset = yf.download('^BVSP','1995-01-27', datetime.date)
plot_acf(asset['Close'], lags=20)
pyplot.show()

plot_pacf(asset['Close'], lags=20)
pyplot.show()