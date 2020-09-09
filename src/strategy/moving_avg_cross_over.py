from .indicators import moving_averages as ma

def ma_crossover(prices):
    """
    baseline, slow, fast: functions that are moving averages
    price: an array of [o,h,l,c] candles
    """
    slow = ma.close(prices[len(prices)-50:])
    fast = ma.close(prices[len(prices)-9:])

    if fast > slow:
        return 'long'
    elif fast < slow:
        return 'short'

    