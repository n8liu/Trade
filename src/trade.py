from strategy import moving_avg_cross_over as strat
from actions import order
from actions import backtest
from actions import graph
from database import dynamodb

def find_trade(pair, strategy):
    if strategy == 'long':
        order.long("EUR_USD", 1000)
    elif strategy == 'short':
        order.short("EUR_USD", 1000)

def maintain_trade(pair, strategy):
    pair_info = order.get_order_info(pair)
    if int(pair_info['currentUnits']) < 0: # if short
        if strategy == 'long':
            order.long(pair, 1000)
    elif int(pair_info['currentUnits']) > 0: # if long
        if strategy == 'short':
            order.short(pair, 1000)
    return None

def back_test(strategy, pair, count, granularity):
    candles = order.get_mid_candles(pair, count, granularity)
    return backtest.backtest(strategy, candles)
    
def trade(strategy, pairs, **kwargs):
    open_pairs = order.get_open_orders()
    for pair in pairs:
        candles = order.get_mid_candles(pair, 50, "M15")
        if pair not in open_pairs:
            find_trade(pair, strategy(candles))
        else:
            maintain_trade(pair, strategy(candles))

trade(strat.ma_crossover, ["EUR_USD"])