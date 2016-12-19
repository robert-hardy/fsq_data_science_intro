# -*- coding: utf-8 -*-
"""
Cleaning the time series from 2015-01-01 onwards

"""

import pandas as pd


# Read the csv back and unstack it.
df_stacked = pd.read_csv('~/spyder/quandl_long_adjclose.csv', header=0)
df = df_stacked.pivot(index="Date", columns="Company", values="Close")

# Restrict to a subset
df = df[df.index > "2015-01-01"]
df.index.min()
df.shape


#
# Sanity checks on the data we have.
#


# (1) How many missing values do we have?
counts = df.count().sort_values()
counts.plot(use_index=False)
counts[:50]

# 420 seems a good cutoff. Which are they?
counts[ counts < 420 ]

# What do they look like?
maybe_exclude_series = df[counts[ counts < 420 ].index.tolist()]
maybe_exclude_series.plot(legend=False)

# Those 5 on the right might be okay. Which are they?
maybe_exclude_series.loc["2016-08-04"]
maybe_exclude_series.loc["2016-08-04"].dropna()
maybe_ok = maybe_exclude_series.loc["2016-08-04"].dropna()

# How do their timeseries look?
df[maybe_ok.index.tolist()].plot(legend=False)

# Final selection.
good_series = maybe_ok.index.tolist() + counts[ counts >= 420 ].index.tolist()
df[good_series].count().sort_values()
df[good_series].count().sort_values().plot(use_index=False)

df = df[good_series]
df.index.min()
df.shape
