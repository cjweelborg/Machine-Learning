# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 02:04:10 2017

@author: Christian
"""

import pandas as pd
import quandl, math, datetime
import numpy as np
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

#########################################################################################
############################ Get the Dataset and Basic Setup ############################
#########################################################################################

# Set the style of the graph
style.use('ggplot')

# Get the stock dataset from quandl
# EOD/KO = Coca Cola Daily Stock
df = quandl.get("EOD/KO", authtoken="vXRsqvDr4iM8Up_pH-7K", start_date="2017-01-01")

# Set the used colums to Adj_Open, Adj_High, Adj_Low, Adj_Close, Adj_Volume
df = df[['Adj_Open','Adj_High','Adj_Low','Adj_Close','Adj_Volume']]

###########################################################################################
############################ Calculations and Set Up Dataframe ############################
###########################################################################################

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

#########################################################################################
############################ Set Up and Train the Classifier ############################
#########################################################################################

# Define the features (typically capital X) as the entire data frame without the label column
# Note: df.drop returns a data frame so we can use df.drop and convert it to a numpy array
X = np.array(df.drop(['label'],1))

# Optional preprocessing : This will scale the training dataset so it is easier to compute
# If scaled, the test data must also be scaled which may result in more overhead and processing in the long run
#X = preprocessing.scale(X)

# This is the data we will actually predict (it doesn't exist yet)
X_lately = X[-predicted_out:]

# Get the X's up until the predicted_out
X = X[:-predicted_out]

# Drops non-existing data
df.dropna(inplace=True)

# Define the labels (typically lowercase y)
y = np.array(df['label'])


# Split the collected data in half
# Create a training dataset and a test dataset from this
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# Choose the algorithm used to compute the prediction
# Create a classifier that uses linear regression
# Set n_jobs=x where x is number of jobs to run (use -1 for max jobs)
clf = LinearRegression()
#clf = svm.SVR(kernel = 'poly')

# Train the classifier with the training dataset
clf.fit(X_train, y_train)

#########################################################################################
############################ Saving and Importing Classifier ############################
#########################################################################################

# Save the classifier so you don't need to re-train the classifier with the data (useful for very large amounts of training data)
with open('linearregression.pickle','wb') as f:
    pickle.dump(clf, f)

# Import the classifier back in from the file
pickle_in = open('linearregression.pickle','rb')

# Define the classifier as the imported pickle file
clf = pickle.load(pickle_in)

####################################################################################################
############################ Testing and Predicting with the Classifier ############################
####################################################################################################

# Test the classifier with the test dataset
accuracy = clf.score(X_test, y_test)

# Print the Accuracy and amount of days out of the predicted set
print("Accuracy for the Predicted Adj_Close %s days out: %s\n" %(predicted_out, accuracy))

# Make a prediction on the next however many days set
predicted_set = clf.predict(X_lately)

# Print out the actual prediction
print(predicted_set)

# Specify the prediction column to being not a number (nan)
df['prediction'] = np.nan

# Get the last date
last_date = df.iloc[-1].name
last_unix = last_date.timestamp()

# Set the day variable = 86400 (Seconds)
one_day = 86400

# Set the next_day
next_unix = last_unix + one_day

# Populate the data frame with the new dates and the prediction values
# Iterate through the predicted set
for i in predicted_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix+= one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]
    
# Plot the points
df['Adj_Close'].plot()
df['prediction'].plot()

# Put the legend in the 4th location (aka bottom right)
plt.legend(loc=4)

# Set the xlabel and ylabel
plt.xlabel('Date')
plt.ylabel('Price')

# Show the graph
plt.show()