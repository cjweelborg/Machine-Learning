# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 17:20:04 2017

@author: Christian
"""

from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import random

# Set the style for the graph to use
style.use('fivethirtyeight')

# Defines x's and y's
# Convert to a numpy array and set the data type
#xs = np.array([1,2,3,4,5,6], dtype=np.float64)
#ys = np.array([5,4,6,5,6,7], dtype=np.float64)

def create_dataset(hm, variance, step=2, correlation=False):
    val = 1
    ys = []
    for i in range(hm):
        y = val + random.randrange(-variance, variance)
        ys.append(y)
        if correlation and correlation == 'pos':
            val += step
        elif correlation and correlation == 'neg':
            val -= step
    xs = [i for i in range(hm)]
    return np.array(xs, dtype=np.float64), np.array(ys, dtype=np.float64)

# Return the m and b values of the line calculated from xs and ys
# Input: xs, ys
# Output: m, b
def best_fit_slope_and_intercept(xs,ys):
    # Calculate the value of the slope (m)
    m = (  ( (mean(xs) * mean(ys)) - mean(xs * ys) ) /
           ( (mean(xs) * mean(xs)) - (mean(xs*xs)) ) )
    
    # Calculate the value of the y-intercept (b)
    b = mean(ys) - (m * mean(xs))
    return m, b

# Return the squared error calculated from the ys_original and ys_line
# Input: ys_orig, ys_line
# Output: squared error of the specific y
def squared_error(ys_orig, ys_line):
    return sum((ys_line - ys_orig)**2)

# This is a calculation that determines how accurate a best fit line is by use of squared error
# Returns the coefficient of determination or r^2
# Input: ys_orig, ys_line
# Output: squared error of the best fit line or coefficient of accuracy of the line
def coefficient_of_determination(ys_orig, ys_line):
    # Calculate the mean of y for every y we have in the original line
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    
    # Calculate the squared error of the regression line
    squared_error_regr = squared_error(ys_orig, ys_line)
    
    # Calculate the squared error of the y_mean_line
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    
    # Now we return the value of R squared error
    return 1 - (squared_error_regr / squared_error_y_mean)


xs, ys = create_dataset(40, 80, 2, correlation='pos')

m,b = best_fit_slope_and_intercept(xs,ys)

#for x in xs:
#    regression_line.append((m*x) + b)
# Is the same as:
regression_line = [(m*x) + b for x in xs]

# Set a value of x to predict y for
predict_x = 8

# Solve for the predict_y using the regression line
predict_y = (m*predict_x)+b

# How good of a fit is our best fit line? Measured with r^2. Higher r^2 values is better.
# R squared  :  r^2 = 1 - ((SE of regression or yhat line)/(SE of mean of y's))  :  SE = Squared Error
r_squared = coefficient_of_determination(ys, regression_line)

# Print out the squared error (r_squared)
print(r_squared)

# Create a scatter plot using the x's and the y's
plt.scatter(xs,ys)

plt.scatter(predict_x,predict_y)

# Plot the points and line on the graph
plt.plot(xs, regression_line)

# Show the graph
plt.show()
