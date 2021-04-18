import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# create simulate data
dates = pd.date_range(datetime.strptime('10/10/2018', '%m/%d/%Y'), periods=11, freq='D')
close_prices = np.arange(len(dates))
close = pd.Series(close_prices, dates)
print("Daily Closing Prices \n{}".format(close))

# use real data
close = pd.read_csv('data.csv', parse_dates=['date'], index_col='date', squeeze=True)

# Pandas Rolling function to provide rolling windows
# it returns a "Rolling" object, similar to the GroupBy object which breaks the original data into groups
# "window" defines the size of the moving window
wd=100
# mean() to get moving average of the window
# get a WD day simple moving average
sma=close.rolling(window=wd).mean()
print("Simple Moving Average of {0} days is \n{1}".format(wd,sma))

# get a WD day weighted moving average 
# pandas doesn't have a off-the-shelf method
weights=np.arange(1,wd+1) # create linear weigths
wma=close.rolling(window=wd).apply(lambda prices:np.dot(prices,weights)/weights.sum(),raw=True)
print("Weighted Linear Moving Average of {0} days is \n{1}".format(wd,wma))

# get a WD day exponential weighted moving average
# we can't simply use 
# ema=close.ewm(span=wd).mean()
# to calculate EWM
# we need make some data modification first as the standard ewm() function is not same as EWM definition
modPrices=close.copy()
modPrices.iloc[0:wd]=sma[0:wd] 
# the "adjust" parameter adjusts the weights to account for the imbalance in the begnning periods.
ema=modPrices.ewm(span=wd, adjust=False).mean()
ema=close.ewm(alpha=0.3).mean()
print("Expontial Weighted Moving Average of {0} days is \n{1}".format(wd,ema))

### compare daily prices, sma, wma in a plot
# WMA is more reactive and floows the price closer than SMA
plt.figure(figsize=(12,6))
plt.plot(close, label="Dailing clsoing price")
plt.plot(sma, label="Simple {}-day moving average".format(wd))
plt.plot(wma, label="Weighted linear {}-day moving avarage".format(wd))
plt.plot(ema, label="Expontial Weighted {}-day moving avarage".format(wd))
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()


def compute_log_returns(prices):
    return np.log(prices) - np.log(prices.shift(1))

print(compute_log_returns(close))
def square_log_returns(rets):
    return rets**2
print(square_log_returns(compute_log_returns(close)))

def estimate_volatility(prices, l):
    """Create an exponential moving average model of the volatility of a stock
    price, and return the most recent (last) volatility estimate.
    
    Parameters
    ----------
    prices : pandas.Series
        A series of adjusted closing prices for a stock.
        
    l : float
        The 'lambda' parameter of the exponential moving average model. Making
        this value smaller will cause the model to weight older terms less 
        relative to more recent terms.
        
    Returns
    -------
    last_vol : float
        The last element of your exponential moving averge volatility model series.
    
    """
    # TODO: Implement the exponential moving average volatility model and return the last value.
    alpha=1-l
    sqr_log_rets=square_log_returns(compute_log_returns(prices))
    ewm=sqr_log_rets.ewm(alpha=alpha).mean()
    sqrt_ewm=ewm**(1/2)
    return sqrt_ewm.iloc[-1]

def test_run(filename='data.csv'):
    """Test run get_most_volatile() with stock prices from a file."""
    prices = pd.read_csv(filename, parse_dates=['date'], index_col='date', squeeze=True)
    print("Most recent volatility estimate: {:.6f}".format(estimate_volatility(prices, 0.7)))

test_run()
