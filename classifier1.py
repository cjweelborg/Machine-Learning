# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 20:30:06 2017

@author: Christian
"""

import pandas as pd
import quandl
import math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

# Get the stock dataset from quandl
# EOD/KO = Coca Cola Daily Stock
df = quandl.get("EOD/KO", authtoken="vXRsqvDr4iM8Up_pH-7K", start_date="2010-01-01", end_date="2017-06-01")

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

print("Accuracy for the Predicted Adj_Close %s days out:" %(predicted_out))

# Shift the predicted_col by the amount of days set in predicted_out so that it shows the predicted days statistics
df['label'] = df[predicted_col].shift(-predicted_out)

# Drops non-existing data
df.dropna(inplace=True)

############## Classifier Stuff ##############

# Define the features (typically capital X) as the entire data frame without the label column
# Note: df.drop returns a data frame so we can use df.drop and convert it to a numpy array
X = np.array(df.drop(['label'],1))

# Define the labels (typically lowercase y)
y = np.array(df['label'])

# Optional preprocessing : This will scale the training dataset so it is easier to compute
# If scaled, the test data must also be scaled which may result in more overhead and processing in the long run
#X = preprocessing.scale(X)

# Split the collected data in half
# Create a training dataset and a test dataset from this
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

# Choose the algorithm used to compute the prediction
# Create a classifier that uses linear regression
# Set n_jobs=x where x is number of jobs to run (use -1 for max jobs)
clf = LinearRegression()
#clf = svm.SVR(kernel = 'poly')

# Train the classifier with the training dataset
clf.fit(X_train, y_train)

# Test the classifier with the test dataset
accuracy = clf.score(X_test, y_test)

print(accuracy)

