# given daily prices for two sample stocks, compute the Volatility (standard deviations of their log returns)

import pandas as pd
import numpy as np

def get_most_volatile(prices):
    """Return the ticker symbol for the most volatile stock.
    
    Parameters
    ----------
    prices : pandas.DataFrame
        a pandas.DataFrame object with columns: ['ticker', 'date', 'price']
    
    Returns
    -------
    ticker : string
        ticker symbol for the most volatile stock
    """
    # TODO: Fill in this function.
    prices_pivot=prices.pivot(index='date',columns='ticker',values='price')
    print(prices_pivot)
    A_v=np.std(prices_pivot['A'].values)
    print(A_v)
    B_v=np.std(prices_pivot['B'].values)
    print(B_v)
    return "A" if A_v > B_v else "B"


def test_run(filename='prices.csv'):
    """Test run get_most_volatile() with stock prices from a file."""
    prices = pd.read_csv(filename, parse_dates=['date'])
    print(prices)
    print(prices.dtypes)
    print("Most volatile stock: {}".format(get_most_volatile(prices)))


test_run()
