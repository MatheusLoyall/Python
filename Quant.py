import numpy as np
import pandas as pd
import xlrd
import openpyxl


## CUSTOM FUNCTIONS ##

def getPrice(tradeTicker):
    priceDf = pd.read_excel(open('H:\Gestão\Estrategias\Estratégias Quant\Propeller\Prices.xlsx','rb'), sheet_name='Prices Ajst',index_col = 0)[tradeTicker]
    priceDf.index = priceDf.index.to_pydatetime()
    priceDf.fillna(method="ffill")
    priceDf = priceDf.astype(float)
    return priceDf

def getPrices():
    priceDf = pd.read_excel(open('H:\Gestão\Estrategias\Estratégias Quant\Propeller\Prices.xlsx','rb'), sheet_name='Prices Ajst', index_col = 0)
    priceDf.index = priceDf.index.to_pydatetime()
    priceDf.fillna(method="ffill")
    priceDf = priceDf.astype(float)
    return priceDf

def m(x, w):
    """Weighted Mean"""
    return np.sum(x * w) / np.sum(w)

def cov(x, y, w):
    """Weighted Covariance"""
    return np.sum(w * (x - m(x, w)) * (y - m(y, w))) / np.sum(w)

def wgtCorr(x, y, w):
    """Weighted Correlation"""
    return cov(x, y, w) / np.sqrt(cov(x, x, w) * cov(y, y, w))

def ewmCorr(x, y, w):
    return np.sum(x * y * w)/(np.sqrt(np.sum(np.square(x)*w))*(np.sqrt(np.sum(np.square(y)*w))))
    
def buildWeights(size, lamb):
    weights = np.repeat(lamb, size)
    weights[0] = 1-lamb
    weights = np.cumprod(weights)
    weights = weights[::-1]
    weightDf = pd.DataFrame({'weights': weights})
    return weightDf

def corrMatrix(prices, x, y, lamb):
    corrMatrix = pd.DataFrame(index=prices.index)
    corrMatrix['corr'] = 0
    weights = buildWeights(100,lamb).values.transpose()
    prices = prices.fillna(method='pad')
    for i in range(1, prices[tradeTicker].size-99):
        defaultPrices = prices[x][i:100+i].values
        shiftedPrices  =  prices[y][i-1:100+i-1].values
        corr = ewmCorr(defaultPrices, shiftedPrices, weights)
        corrMatrix.ix[i+99, 'corr'] = corr
    return corrMatrix


def corrModel(tradeTicker, startdate, enddate, tickers, lamb, minCorr, minRet, auto_signals):
     
    data = ['PX_LAST', 'PX_HIGH', 'LOW']

    main_price = getPrice(tradeTicker)

    prices = pd.DataFrame(index=main_price.index)

    prices[tradeTicker]      =  main_price
    prices['BZACCETP Index'] =  getPrice('BZACCETP Index')
    prices['IBOV Index']     =  getPrice('IBOV Index')
    prices['BRL Curncy']     =  getPrice('BRL Curncy')

    prices = prices[prices.index.weekday==4]

    prices[tradeTicker + '_log_returns'] = np.log(1.0+ prices[tradeTicker].pct_change())
    prices[tradeTicker + '_log_returns'][0] = 0
    prices['ewm_correlations'] = corrMatrix(prices, tradeTicker + '_log_returns', tradeTicker + '_log_returns', lamb)
    if(auto_signals):
        prices['auto_signals'] = np.sign(np.nan_to_num(prices['ewm_correlations'].where(np.absolute(prices['ewm_correlations']) > minCorr))) * np.sign(np.nan_to_num(prices[tradeTicker + '_log_returns'].where(np.absolute(prices[tradeTicker + '_log_returns']) > minRet)))

    for ticker in tickers:
       prices[ticker] = getPrice(ticker)
       ticker_calc = ticker + "_log_returns"
       prices[ticker_calc] = np.log(1+ prices[ticker].pct_change())
       prices[ticker_calc][0] = 0
       corr_matrix = corrMatrix(prices, tradeTicker + '_log_returns', ticker_calc, lamb)
       prices[ticker+'_correl'] = corr_matrix
       prices[ticker+'_signals'] = np.sign(np.nan_to_num(prices[ticker+'_correl'].where(np.absolute(prices[ticker+'_correl']) > minCorr))) * np.sign(np.nan_to_num(prices[ticker_calc].where(np.absolute(prices[ticker_calc]) > minRet)))
    
    prices['signal'] = 0
    if (auto_signals):
        prices['signal'] = prices['signal'] + prices['auto_signals']
    for ticker in tickers:
        prices['signal'] = prices['signal'] + prices[ticker + '_signals']

    prices['signal'] = np.sign(prices['signal'])

    prices['positions'] = np.sign(prices['signal'].diff())
    prices['returns'] = prices['signal'].shift(1) * prices[tradeTicker].pct_change()
    prices['total'] = prices['positions'].cumsum() * prices[tradeTicker]

    prices['CDI'] = (1+prices['BZACCETP Index'].pct_change())
    prices['cota_CDI'] = prices['CDI'].cumprod()
    prices['cota_CDI'][0] = 1

    adm = 1-0.02/(252/21)

    prices['cota_return'] = ((prices['returns']+1)*prices['CDI']*adm)
    trading_costs = (1 - 0.003*prices['positions'].abs()).cumprod()
    prices['cota'] = prices['cota_return'].cumprod()*trading_costs
    prices['cota'][0] = 1

    return prices

def MAModel(tradeTicker, startdate, enddate, data, short_window, long_window, short_enable, tolerance, weekly):
    
    main_price = getPrice(tradeTicker)

    prices = pd.DataFrame(index=main_price.index)

    prices[tradeTicker]      =  main_price
    prices['BZACCETP INDEX'] =  getPrice('BZACCETP Index')
    prices['BRL Curncy']     =  getPrice('BRL Curncy')

    prices['signal'] = 0.0
    prices['signal1'] = 0.0
    prices['signal2'] = 0.0

    if(weekly):
        prices = prices[prices.index.weekday==4]    

    # Create the set of short and long simple moving averages over the 
    # respective periods
    prices['short_mavg'] = prices[tradeTicker].rolling( window=short_window).mean()
    prices['long_mavg'] = prices[tradeTicker].rolling( window=long_window).mean()

    prices['lower_band'] = prices[tradeTicker].rolling( window=short_window).mean() - 2*prices[tradeTicker].rolling( window=short_window).std()
    prices['higher_band'] = prices[tradeTicker].rolling( window=short_window).mean() + 2*prices[tradeTicker].rolling( window=short_window).std()

    # prices['short_mavg'] = prices[tradeTicker].ewm( min_periods=1, adjust=False, alpha=(2/(short_window+1))).mean()
    # prices['long_mavg'] = prices[tradeTicker].ewm( min_periods=1, adjust=False, alpha=(2/(long_window+1))).mean()

    # Create a 'signal' (invested or not invested) when the short moving average crosses the long
    # moving average, but only for the period greater than the shortest moving average window

    prices['signal1'][short_window:] = np.where(((
        prices['short_mavg'][short_window:]-prices['long_mavg'][short_window:])/prices['short_mavg'][short_window:]).abs() > tolerance,
        np.where(prices['short_mavg'][short_window:]> prices['long_mavg'][short_window:], 1.0, -1.0) , -0.0)

    prices['signal2'][short_window:] = np.where(prices[tradeTicker][short_window:] 
        < prices['lower_band'][short_window:], 1.0, np.where(prices[tradeTicker][short_window:] 
        > prices['higher_band'][short_window:], -0.0, 0))

    prices['signal'] = np.sign(prices['signal1'] + prices['signal2'])


            # Take the difference of the signals in order to generate actual trading orders
    prices['positions'] = np.sign(prices['signal'].diff())
    prices['returns'] = prices['signal'] * prices[tradeTicker].shift(-1).pct_change()
    prices['total'] = prices['positions'].cumsum() * prices[tradeTicker]

    prices['CDI'] = (1+prices['BZACCETP INDEX'].pct_change())
    prices['cota_CDI'] = prices['CDI'].cumprod()
    prices['cota_CDI'][0] = 1

    adm = 1-0.02/252

    if(weekly):
        adm = 1-0.02/(252/5)

    prices['cota_return'] = ((prices['returns']+1)*prices['CDI']*adm)
    trading_costs = (1 - 0.003*prices['positions'].abs()).cumprod()
    prices['cota'] = prices['cota_return'].cumprod()*trading_costs
    prices['cota'][0] = 1

    return prices


## MAIN -- Bolsa ##

writer = pd.ExcelWriter('H:\Gestão\Estrategias\Quant\Propeller\Sinais.xlsx')

startdate = '19960419'
enddate = '20180102'

tradeTicker = 'BZ1 A:00_0_R Index'
tickers = ['AUD Curncy', 'XPT Curncy','BRL Curncy']
lamb = 0.18
minCorr = 0.28
minRet = 0.002

modelOutput33 = corrModel(tradeTicker, startdate, enddate, tickers, lamb, minCorr, minRet, False)
modelOutput33.loc[modelOutput33['signal'] == -1, 'signal'] = 0

modelOutput33[['signal', 'AUD Curncy_signals', 'AUD Curncy_correl', 'XPT Curncy_signals', 'XPT Curncy_correl', 'BRL Curncy_signals', 'BRL Curncy_correl']].to_excel(writer, "Bolsa Semanal")

## MAIN -- Dólar ##

data = ['PX_LAST']
tradeTicker = 'BRL Curncy'

modelOutput1 = MAModel(tradeTicker, startdate, enddate, data, 5, 30, True, 0.00, False)

modelOutput1.to_excel(writer, "Dólar Diário")

##modelOutput1.to_excel(writer, tradeTicker.replace(":","")+"5_30_0")

dailyDataFrame = pd.DataFrame
dailyData = getPrice('UC1 A:00_0_R Curncy') 

dailyDataFrame = pd.DataFrame(index=dailyData.index)

dailyDataFrame['BZACCETP INDEX'] 	=  getPrice('BZACCETP Index')
dailyDataFrame['BZ1 Index'] 		=  getPrice('BZ1 A:00_0_R Index')
dailyDataFrame['UC1 Curncy'] 		=  getPrice('UC1 A:00_0_R Curncy')
dailyDataFrame['BRL Curncy'] 		=  getPrice('BRL Curncy')
dailyDataFrame['IBOV Index'] 		=  getPrice('IBOV Index')

dailyDataFrame.groupby([lambda x: x.year,lambda x: x.month]).last()

dailyDataFrame.to_excel(writer, 'data')

monhtlyDf = dailyDataFrame.groupby([lambda x: x.year,lambda x: x.month]).last()

monhtlyDf.to_excel(writer, 'data_monthly')

# dt = pd.read_excel(open('di_Futuro2.xlsx','rb'), sheetname='data')

# tradeTicker = 'data'
# tickers = ['data']
# lamb = 0.18
# minCorr = 0.28
# minRet = 0.001

# modelOutput2 = corrModel2(dt, lamb, minCorr, minRet, True)
# modelOutput2.to_excel(writer, "DI")


writer.save()



