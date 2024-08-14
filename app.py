import numpy as np
import pandas as pd

ser = pd.Series(np.random.random(5), name='column 1')

ser

# importar dados de multipals ações usando yfinance 
import yfinance as yf
import pandas

tickers = ['PG', 'MSFT', 'T', 'F', 'GE']
new_data = pandas.DataFrame(columns=tickers)
for i in tickers:
    new_data[i] = yf.download(i, start='1995-1-1')['Adj Close']
new_data.tail()
