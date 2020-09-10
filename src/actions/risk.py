def average_true_range(array):
    """ Measures market volatility.

    How to read: 0.0003 is 3 pips, 0.01 is 1 pip for JPY

    Formula (according to Investopedia):
        Average True Range = sum(True Range) / period
        True Range (per candle) = Max[(high - low), Abs(high - close), Abs(low - close)]

    Args:
        array: a list of [open,high,low,close] candles, where the length
               of the array corresponds to the period.
    
    Returns: 
        an Integer representing the ATR in pips.
    """
    tr_sum = 0
    for i in range(len(array)):
        tr_sum += max(abs(array[i][1] - array[i][2]), abs(array[i][1] - array[i][3]), abs(array[i][2] - array[i][3]))
    atr = tr_sum / len(array)
    return atr