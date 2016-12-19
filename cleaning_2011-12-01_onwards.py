# -*- coding: utf-8 -*-
"""
Cleaning the 5y time series

"""

import pandas as pd


# Read the csv back and unstack it.
df_stacked = pd.read_csv('~/spyder/quandl_long_adjclose.csv', header=0)
df = df_stacked.pivot(index="Date", columns="Company", values="Close")
df.index.min()
df.shape

# Make sure Pandas recognizes the index as dates
df.index = pd.to_datetime(df.index)


#
# Sanity checks on the data we have.
#


# (1) How many missing values do we have?
df.count().sort_values().plot(use_index=False)

# Not so easy to decide this time.
# 1200 seems a reasonable cutoff but is there a better way to choose?
# Let's count by year
cg = pd.groupby(df, by=[df.index.year])
cgs = cg.count()
cgs.iloc[:, :5]

cgs.index.name = "Year"
cgs.plot(legend=False)

mask = (cgs.loc[2016] >= 200)
f = cgs.loc[:,mask]
f.plot(legend=False)
f.shape

mask = (cgs.loc[2016] >= 200) & (cgs.loc[2015] >= 200)
f = cgs.loc[:,mask]
f.plot(legend=False)
f.shape

mask = (cgs.loc[2016] >= 200) & (cgs.loc[2015] >= 200) & (cgs.loc[2014] >= 200)
f = cgs.loc[:,mask]
f.plot(legend=False)
f.shape

# It's interesting to see the count plots side by side
dff = df[f.columns]
dff.count().sort_values().plot(use_index=False)
df.count().sort_values().plot(use_index=False)

df = dff
df.plot(legend=False)


# (2) Checking for jumps that might be errors
# Looking at the biggest percentage jumps
(df.diff(1) / df.shift(1)).abs().max().sort_values()
mask = (df.diff(1) / df.shift(1)).abs().max() > 0.7
df.loc[:, mask].plot().legend(loc='center left', bbox_to_anchor=(1, 0.5))

# This one looks like the split has not been taken into the Adj. Close
# Go see: https://www.splithistory.com/hbi/
# HanesBrands (HBI) has 1 split in our HBI split history database.
# The split for HBI took place on March 04, 2015.
# This was a 4 for 1 split.

# 5 companies had a 1-day drop over 50%
# but not all were splits (PPG and Hanesbrands yes).
(df.diff(1) / df.shift(1)).min().sort_values(ascending=False)
mask = (df.diff(1) / df.shift(1)).min() < -0.5
df.loc[:, mask].plot().legend(loc='center left', bbox_to_anchor=(1, 0.5))


# Stocks that have had quite a few big 1-day jumps
mask = (df.diff(1) / df.shift(1)) > 0.1
mask.sum().sort_values()
colmask = mask.sum() >= 10
df.loc[:, colmask].plot().legend(loc='center left', bbox_to_anchor=(1, 0.5))