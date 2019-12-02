import pandas as pd

# read file
price_df = pd.read_csv('prices.csv', names=['ticker', 'date', 'open', 'high', 'low',
                                             'close', 'volume', 'adj_close', 'adj_volume'])
print(price_df)


##### DataFrame Calculations

# calculate median value by grouping "ticker"
print(price_df.groupby('ticker').median())

# DataFrame 2 dimensions to 3 dimensions
open_prices = price_df.pivot(index='date', columns='ticker', values='open')
print(open_prices)
print(open_prices.mean())

# get mean for each date by doing a transpose
print(open_prices.T.mean())