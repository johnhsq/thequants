import pandas as pd
from datetime import timedelta

month = pd.to_datetime('02/01/2018')
close_month = pd.DataFrame(
    {
        'A': 1,
        'B': 12,
        'C': 35,
        'D': 3,
        'E': 79,
        'F': 2,
        'G': 15,
        'H': 59},
    [month])

print(close_month)

print(close_month.loc[month].nlargest(2))   # top 2 performers
print(close_month.loc[month].nsmallest(2))  # bottom 2 performers




day1 = pd.to_datetime('07/08/2013')
day2 = day1 + timedelta(days=1)
prices = pd.DataFrame(
    {
        'A': [2,5],
        'B': [2,3],
        'C': [7,6],
        'D': [2,7],
        'E': [6,5],},
    [day1,day2])
print(prices)

sector = pd.Series(
    ["Utilities","Health Care", "Real Estate", "Real Estate", "Information Technology"],
    index=["A","B","C","D","E"]
)
print(sector)

# find the top performing closing prices and return their sectors for a single date.
def date_top_industries(prices, sector, date, top_n):
    """
    Get the set of the top industries for the date
    
    Parameters
    ----------
    prices : DataFrame
        Prices for each ticker and date
    sector : Series
        Sector name for each ticker
    date : Date
        Date to get the top performers
    top_n : int
        Number of top performers to get
    
    Returns
    -------
    top_industries : set
        Top industries for the date
    """
    # TODO: Implement Function

    stocks=prices.loc[date].nlargest(top_n)
    ret=set(sector.loc[stocks.index])
    return ret

print(date_top_industries(prices, sector, day2, 3))     # return {"Utilities", "Real Estate"}