# -*- coding: utf-8 -*-
"""
Loading data from Quandl
"""

import pandas as pd
import quandl
quandl.ApiConfig.api_key = 'your API key'

data = quandl.get("WIKI/MMM", start_date="2011-12-01", type="raw")
data["Adj. Close"].plot().legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Get the names and tickers of the S&P 500 constituents
snp_constituents = pd.read_csv("https://s3.amazonaws.com/static.quandl.com/tickers/SP500.csv")
snp_constituents["free_code"] = snp_constituents["free_code"].apply(lambda s: s.replace("-", "_"))


# Get the price histories
dct = {}
for idx, row in snp_constituents[:5].iterrows():
    data = quandl.get(row["free_code"], start_date="2016-12-01", type="raw")
    dct[row["name"]] = data["Adj. Close"]    # NB not data[["Close""]]


# Join them all together and write the stacked format as a csv file.
df = pd.concat(dct, axis=1)
df.columns.name = "Company"
df_stacked = df.stack().reset_index()
df_stacked.index.name = "Index"
df_stacked.columns = ["Date", "Company", "Close"]
df_stacked.to_csv('~/spyder/quandl_foo.csv', header=True)
