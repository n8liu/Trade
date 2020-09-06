""" Contains all moving averages.

Lists several moving average functions, including simple moving averages
and exponential moving averages. These can be placed on top of other indicators
to make things happen. Most baselines will be some type of moving average.
"""

import numpy as np

""" Simple Moving Averages

Calculates by adding the values of each index and dividing by the length of 
the array.

Returns:
    a single float representing the average of the given list.  
"""
def high(array):
    """see Simple Moving Average docstring
    
    Calculated using the high price of each candle [o,h,l,c]. 
    """
    return sum([candle[1] for candle in array]) / len(array)
    # sum all candle high prices in array and divide by array length
    
def low(array):
    """see Simple Moving Average docstring
    
    Calculated using the low price of each candle [o,h,l,c]. 
    """
    return sum([candle[2] for candle in array]) / len(array)
    # sum all candle low prices in array and divide by array length

def close(array):
    """see Simple Moving Average docstring
    
    Calculated using the closing price of each candle [o,h,l,c]. 
    """
    return sum([candle[3] for candle in array]) / len(array) 
    # sum all candle close prices in array and divide by array length