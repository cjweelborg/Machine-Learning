# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 21:19:43 2017

@author: Christian
"""

import pandas as pd
import quandl
import math

# Get the stock dataset from quandl
# EOD/KO = Coca Cola Daily Stock
df = quandl.get("EOD/KO", authtoken="vXRsqvDr4iM8Up_pH-7K", start_date="2016-01-01", end_date="2017-06-01")

# Set the used colums to Adj_Open, Adj_High, Adj_Low, Adj_Close, Adj_Volume
df = df[['Adj_Open','Adj_High','Adj_Low','Adj_Close','Adj_Volume']]


############## Calculate new columns from the known data ##############

# HighLow Percent change ex. (High - Low) / Low * 100 = PCT change between high and low
df['HL_PCT'] = (df['Adj_High'] - df['Adj_Low']) / df['Adj_Low'] * 100.0

# Percent change of the stock ex. (New - Old) / Old * 100 = PCT change
df['PCT_change'] = (df['Adj_Close'] - df['Adj_Open']) / df['Adj_Open'] * 100.0


# Set the new columns we care about after calculations
df = df[['Adj_Close', 'HL_PCT', 'PCT_change', 'Adj_Volume']]


# Set the Predicted column : This can be anything you want to predict
predicted_col = 'Adj_Close'

# Fill the blank data with -99999 so it will act as an outlier rather than get rid of the data
df.fillna(-99999, inplace=True)

# Predict a certain percent of days out 0.01 = 1 percent of days out : 0.1 = 10 percent of days out
# The math (DECIMAL) * length of the data frame = (DECIMAL * 100) Percent days of the data frame as the data frame length is the total amount of days between start date and end date
predicted_out = int(math.ceil(0.01*len(df)))

# Shift the predicted_col by the amount of days set in predicted_out so that it shows the predicted days statistics
df['label'] = df[predicted_col].shift(-predicted_out)

# Drops non-existing data
df.dropna(inplace=True)

# Print out the last columns of the dataset
print(df.tail())