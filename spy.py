#!/usr/bin/env python3

# install these packages with pip:
#   - pandas
#   - yfinance
#   - plotly

import os
import pandas as pd
import time
import plotly.express as px

filename = 'stock_data.csv'

def download_stocks():
    import yfinance as yf
    import datetime
    import operator

    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', header=0)[0]
    tickers_list = table.Symbol.to_list()

    # Define today
    today = datetime.date.today()

    # Define date 6 months ago
    six_months_ago = today - datetime.timedelta(days=6*30)  # Approximation

    # Fetch the data
    data = yf.download(tickers_list, six_months_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

    # assuming 'data' is your DataFrame
    returns = {}

    # Calculating price return for each stock
    for stock in tickers_list:
        initial_price = data['Adj Close'][stock].iloc[0]
        final_price = data['Adj Close'][stock].iloc[-1]
        price_return = ((final_price - initial_price) / initial_price) * 100
        if price_return == price_return:
            returns[stock] = price_return

    return returns

def is_file_empty(filename):
    with open(filename, 'r') as f:
        if f.read().strip():
            return False
        else:
            return True

def is_file_outdated(filename, days=1):
    current_time = time.time()
    file_modification_time = os.path.getmtime(filename)
    return (current_time - file_modification_time) > (days * 86400)

if os.path.isfile(filename) and not is_file_outdated(filename) and not is_file_empty(filename):
    returns = pd.read_csv(filename)
else:
    import csv
    stock_data = download_stocks()
    print(list(stock_data.items()))
    returns = pd.DataFrame(list(stock_data.items()), columns=["Stock", "Return"])
    returns = returns.sort_values(by='Return', ascending=False)
    returns.to_csv(filename, index=False)

pd.set_option('display.max_rows', None)  # Disable row truncation
pd.set_option('display.width', None)     # Disable column width truncation

print(returns.sort_values(by='Return', ascending=True).to_string(index=False))


# Create a bar chart using Plotly
fig = px.bar(returns, x='Stock', y='Return', title='S&P 500 Stock Returns (6 Months)',
             labels={'Stock': 'Stock Symbol', 'Return': 'Return (%)'},
             color='Return', color_continuous_scale='Viridis')

# Show the plot
fig.show()
