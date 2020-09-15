from .indicators import moving_averages as ma

def ma_crossover(prices, **kwargs):
    """
    baseline, slow, fast: functions that are moving averages
    price: an array of [o,h,l,c] candles
    """
    strategy_name = '9 and 50 moving average crossover'
    decision = 'wait'
    slow = ma.close(prices[len(prices)-50:])
    fast = ma.close(prices[len(prices)-9:])
    if fast > slow:
        decision = 'long'
    elif fast < slow:
        decision = 'short'
    return decision

    