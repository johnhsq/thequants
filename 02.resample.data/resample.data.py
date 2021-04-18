import numpy as np
import pandas as pd

dates = pd.date_range('10/10/2018', periods=11, freq='D')
close_prices = np.arange(len(dates))

close = pd.Series(close_prices, dates)
print(dates)
print(close_prices)
print(close)
print('-'*50)

# resample data every 3days with the first data
print(close.resample('3D').first())

print(
    pd.DataFrame({
        'days': close,
        'weeks': close.resample('W').first()
    })
)

print('-'*50)
print(close.resample('W').max())