import pandas as pd
import numpy as np
import os
from statsmodels.tsa.arima_model import ARMA
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
#note that for the figure size to show, this cell should be run
#separately from the import of pyplot
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (14, 8)

### Simulate return series with autoregressive properties
from statsmodels.tsa.arima_process import ArmaProcess
np.random.seed(200)

# ARMA: AutoRegressive Moving Average
ar_params = np.array([1, -0.5])
ma_params = np.array([1, -0.3])
ret = ArmaProcess(ar_params, ma_params).generate_sample(nsample=5*252)

ret = pd.Series(ret)
drift = 100
price = pd.Series(np.cumsum(ret)) + drift

# simulated return series
ret.plot(figsize=(15,6), color=sns.xkcd_rgb["pale purple"], title="simulated return series")
plt.show()

# simulated price series
price.plot(figsize=(15,6), color=sns.xkcd_rgb["baby blue"], title="simulated price series")
plt.show()

# Log returns
lret = np.log(price) - np.log(price.shift(1))
lret = lret[1:]

### autocorrelation
# Use autocorrelation to get a sense of what lag to use for the autoregressive model.
from statsmodels.graphics.tsaplots import plot_acf
_ = plot_acf(lret,lags=10, title='log return autocorrelation')
plt.show()

# plot partial autocorrelation
# Partial autocorrelation is different from autocorrelation in that 
# it shows the influence of each period that is not attributed to the other periods leading up to the current period. 
# In other words, the two-day lag had a fairly strong correlation with the current value 
# because it had a strong correlation with the one-day lag. 
# However, the two-day lag's partial correlation with the current period that isn't attributable to the one-day lag is relatively small.
from statsmodels.graphics.tsaplots import plot_pacf
_ = plot_pacf(lret, lags=10, title='log return Partial Autocorrelation', color=sns.xkcd_rgb["crimson"])
plt.show()


### Ljung-Box Test
# The Ljung-Box test helps us check whether the lag we chose gives autocorrelations that are significantly different from zero. 
# The null hypothesis is that the previous lags as a whole are not correlated with the current period. 
# If the p-value is small enough (say 0.05), we can reject the null and assume that the past lags have some correlation with the current period.
from statsmodels.stats.diagnostic import acorr_ljungbox
lb_test_stat, lb_p_value = acorr_ljungbox(lret,lags=20)
# the Ljung-Box test shows p-values less than 0.05 for the 20 lag periods that we tested.
print(lb_p_value)

### Fit an ARMA model
# We'll just use one lag for the autoregression and one lag for the moving average.
from statsmodels.tsa.arima_model import ARMA
AR_lag_p = 1
MA_lag_q = 1
order = (AR_lag_p, MA_lag_q)
arma_model = ARMA(lret.values, order=order)
arma_result = arma_model.fit()
arma_pred = pd.Series(arma_result.fittedvalues)
# View fitted predictions against actual values
plt.plot(lret, color=sns.xkcd_rgb["pale purple"])
plt.plot(arma_pred, color=sns.xkcd_rgb["dark sky blue"])
plt.title('Log returns and predictions using an ARMA(p=1,q=1) model');
# Fitted AR parameter 0.65, MA parameter -0.45
print(f"Fitted AR parameter {arma_result.arparams[0]:.2f}, MA parameter {arma_result.maparams[0]:.2f}")
plt.show()

### In general, autoregressive moving average models are not able to forecast stock returns because stock returns are non-stationary and also quite noisy.


### ARIMA
# Fit an AutoRegressive Integrated Moving Average model. Choose an order of integration of 1, autoregresion lag of 1, and moving average lag of 1.
from statsmodels.tsa.arima_model import ARIMA
def fit_arima(lret):
    
    #TODO: choose autoregression lag of 1
    AR_lag_p = 1
    
    #TODO: choose moving average lag of 1
    MA_lag_q = 1
    
    #TODO: choose order of integration 1
    order_of_integration_d = 1
    
    #TODO: Create a tuple of p,d,q
    order = (AR_lag_p, order_of_integration_d, MA_lag_q)
    
    #TODO: create an ARIMA model object, passing in the values of the lret pandas series,
    # and the tuple containing the (p,d,q) order arguments
    arima_model = ARIMA(lret.values, order=order)
    
    arima_result = arima_model.fit()
    
    #TODO: from the result of calling ARIMA.fit(),
    # save and return the fitted values, autoregression parameters, and moving average parameters
    fittedvalues = arima_result.fittedvalues
    arparams =  arima_result.arparams
    maparams =  arima_result.maparams
   
    return fittedvalues,arparams,maparams

fittedvalues,arparams,maparams = fit_arima(lret)
arima_pred = pd.Series(fittedvalues)
plt.plot(lret, color=sns.xkcd_rgb["pale purple"])
plt.plot(arima_pred, color=sns.xkcd_rgb["jade green"])
plt.title('Log Returns and predictions using an ARIMA(p=1,d=1,q=1) model')
print(f"fitted AR parameter {arparams[0]:.2f}, MA parameter {maparams[0]:.2f}")

