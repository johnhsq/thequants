# install packages
# If you’re using an enhanced shell like IPython or the Jupyter notebook, you can run system commands like those in this tutorial by prefacing them with a ! character:
# import sys
# !{sys.executable} - m pip install -r requirements.txt

# load packages
import pandas as pd
import numpy as np
import helper
import project_helper
import project_tests

#load data
df = pd.read_csv('/Users/huang/Documents/Workspace/thequants/05.trading/eod-quotemedia.csv', parse_dates=['date'], index_col=False)
print(df)
close = df.reset_index().pivot(index='date', columns='ticker', values='adj_close')
print(close)

# view data
project_helper.print_dataframe(close)

apple_ticker = 'AAPL'
project_helper.plot_stock(close[apple_ticker], '{} Stock'.format(apple_ticker))

# resample the data from daily to month end
def resample_prices(close_prices, freq='M'):
    """
    Resample close prices for each ticker at specified frequency.
    
    Parameters
    ----------
    close_prices : DataFrame
        Close prices for each ticker and date
    freq : str
        What frequency to sample at
        For valid freq choices, see http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    
    Returns
    -------
    prices_resampled : DataFrame
        Resampled prices for each ticker and date
    """
    # TODO: Implement Function
    
    return close_prices.resample('M').last()

# unit test resample_prices()
project_tests.test_resample_prices(resample_prices)

# view month end data vs daily data
monthly_close = resample_prices(close)
print("============Month End Close Price ")
print(monthly_close.loc[:, apple_ticker])
project_helper.plot_resampled_prices(
    monthly_close.loc[:, apple_ticker],
    close.loc[:, apple_ticker],
    '{} Stock - Close Vs Monthly Close'.format(apple_ticker))

# Compute log returns ( 𝑅𝑡 ) from prices ( 𝑃𝑡 ) as your primary momentum indicator:
# 𝑅𝑡=𝑙𝑜𝑔𝑒(𝑃𝑡)−𝑙𝑜𝑔𝑒(𝑃𝑡−1)
def compute_log_returns(prices):
    """
    Compute log returns for each ticker.
    
    Parameters
    ----------
    prices : DataFrame
        Prices for each ticker and date
    
    Returns
    -------
    log_returns : DataFrame
        Log returns for each ticker and date
    """
    # TODO: Implement Function
    return np.log(prices) - np.log(prices.shift(1))
# unit test
project_tests.test_compute_log_returns(compute_log_returns)

# View Log Returns of AAPL Stock (Monthly)
monthly_close_returns = compute_log_returns(monthly_close)
project_helper.plot_returns(
    monthly_close_returns.loc[:, apple_ticker],
    'Log Returns of {} Stock (Monthly)'.format(apple_ticker))

# Shift Returns
# if shift_n=2, means the return will be shift to 2 (days or months) later
def shift_returns(returns, shift_n):
    """
    Generate shifted returns
    
    Parameters
    ----------
    returns : DataFrame
        Returns for each ticker and date
    shift_n : int
        Number of periods to move, can be positive or negative
    
    Returns
    -------
    shifted_returns : DataFrame
        Shifted returns for each ticker and date
    """
    # TODO: Implement Function
    
    return returns.shift(shift_n)
# unit test
project_tests.test_shift_returns(shift_returns)


# View previous months and next month's return
prev_returns = shift_returns(monthly_close_returns, 1)
lookahead_returns = shift_returns(monthly_close_returns, -1)
print('======================= all returns start')
print(prev_returns)
print(monthly_close_returns)
print(lookahead_returns)
print('======================= all returns end')

project_helper.plot_shifted_returns(
    prev_returns.loc[:, apple_ticker],
    monthly_close_returns.loc[:, apple_ticker],
    'Previous Returns of {} Stock'.format(apple_ticker))
project_helper.plot_shifted_returns(
    lookahead_returns.loc[:, apple_ticker],
    monthly_close_returns.loc[:, apple_ticker],
    'Lookahead Returns of {} Stock'.format(apple_ticker))

##### Generate Trading Signal
### Trading Strategy
# For each month-end observation period, rank the stocks by previous returns, 
# from the highest to the lowest. Select the top performing stocks for the long portfolio, 
# and the bottom performing stocks for the short portfolio.
def get_top_n(prev_returns, top_n):
    """
    Select the top performing stocks
    
    Parameters
    ----------
    prev_returns : DataFrame
        Previous shifted returns for each ticker and date
    top_n : int
        The number of top performing stocks to get
    
    Returns
    -------
    top_stocks : DataFrame
        Top stocks for each ticker and date marked with a 1
    """
    temp_pd=prev_returns.copy()
    temp_pd[:]=0
    temp_pd=temp_pd.astype('int64')
    for index, row in prev_returns.iterrows():
        for item in row.nlargest(top_n).iteritems():
            temp_pd.loc[index,item[0]]=1
    # TODO: Implement Function
    prev_returns=temp_pd
    return prev_returns
# unit test
project_tests.test_get_top_n(get_top_n)


# View Data: the best and worst performing stocks
# To get the best performing stocks, we'll use the get_top_n function. 
# To get the worst performing stocks, we'll also use the get_top_n function. However, we pass in -1*prev_returns instead of just prev_returns.
top_bottom_n = 50
df_long = get_top_n(prev_returns, top_bottom_n)
df_short = get_top_n(-1*prev_returns, top_bottom_n)
print("======================= df_long")
print(df_long)
print("======================= df_short")
print(df_short)
project_helper.print_top(df_long, 'Longed Stocks',top_n=10)
project_helper.print_top(df_short, 'Shorted Stocks', top_n=10)


##### Project Returns:  check if your trading signal has the potential to become profitable!
# 1. compute the net returns this portfolio would return; assume every stock gets an equal dollar amount of investment
# compute the expected portfolio returns
# lookahead_returns: means I predict what my returns is one month ahead
# for example:
# 7/31/2018: AAPL 100
# 8/31/2018: AAPL 110
# monthly return on 8/31/2018 is 10%
# lookahead return on 7/31/2018 is 10% (on 7/31 I will expext 10% return this month)
def portfolio_returns(df_long, df_short, lookahead_returns, n_stocks):
    """
    Compute expected returns for the portfolio, assuming equal investment in each long/short stock.
    
    Parameters
    ----------
    df_long : DataFrame
        Top stocks for each ticker and date marked with a 1
    df_short : DataFrame
        Bottom stocks for each ticker and date marked with a 1
    lookahead_returns : DataFrame
        Lookahead returns for each ticker and date
    n_stocks: int
        The number number of stocks chosen for each month
    
    Returns
    -------
    portfolio_returns : DataFrame
        Expected portfolio returns for each ticker and date
    """
    
    # TODO: Implement Function
    
    return (df_long/n_stocks-df_short/n_stocks)*lookahead_returns
# unit test
project_tests.test_portfolio_returns(portfolio_returns)

print("============================ portfolio_returns()")
expected_portfolio_returns = portfolio_returns(df_long, df_short, lookahead_returns, 2*top_bottom_n)
print(expected_portfolio_returns)
project_helper.plot_returns(expected_portfolio_returns.T.sum(), 'Portfolio Returns')


# Annualized Rate of Return
expected_portfolio_returns_by_date = expected_portfolio_returns.T.sum().dropna()
portfolio_ret_mean = expected_portfolio_returns_by_date.mean()
portfolio_ret_ste = expected_portfolio_returns_by_date.sem()
portfolio_ret_annual_rate = (np.exp(portfolio_ret_mean * 12) - 1) * 100

print("""
Mean:                       {:.6f}
Standard Error:             {:.6f}
Annualized Rate of Return:  {:.2f}%
""".format(portfolio_ret_mean, portfolio_ret_ste, portfolio_ret_annual_rate))


##### T-Test
# Our null hypothesis ( 𝐻0 ) is that the actual mean return from the signal is zero. 
# We'll perform a one-sample, one-sided t-test on the observed mean return, to see if we can reject  𝐻0 .
# 0. Set 𝛼=0.05
# 1. compute the t-statistic
# 2. find its corresponding p-value
# 3. if p-value< 𝛼 means that the chance of observing the mean we observed under the null hypothesis is small, and thus casts doubt on the null hypothesis
from scipy import stats

def analyze_alpha(expected_portfolio_returns_by_date):
    """
    Perform a t-test with the null hypothesis being that the expected mean return is zero.
    
    Parameters
    ----------
    expected_portfolio_returns_by_date : Pandas Series
        Expected portfolio returns for each date
    
    Returns
    -------
    t_value
        T-statistic from t-test
    p_value
        Corresponding p-value
    """
    # TODO: Implement Function
    null_hypothesis = 0.0
    t,p= stats.ttest_1samp(expected_portfolio_returns_by_date, null_hypothesis, axis=0)
    return t,p/2
# unit test
project_tests.test_analyze_alpha(analyze_alpha)

# view data
t_value, p_value = analyze_alpha(expected_portfolio_returns_by_date)
print("""
    Alpha analysis:
    t-value:        {:.3f}
    p-value:        {:.6f}
    """.format(t_value, p_value))

print("""
    Conclusion:
    p-value is {:.6f} > alpha (0.05). 
    We can't reject null hypothesis, meaning the return is statistially close to zero
    """.format(p_value))