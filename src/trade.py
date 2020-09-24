import time
from actions import order
from actions import backtest
from actions import graph
from indicators import average_true_range as atr
from indicators import ssl

def find_trade(pair, strategy, candles):
    if strategy == 'long':
        status = order.long(pair, 1000)
    elif strategy == 'short':
        status = order.short(pair, 1000)
    else:
        return "No order placed"
    
    if status == 201:
        '''average_true_range.atr(candles[-14:])'''
        if order.is_order_open(pair):
            order.create_take_profit(pair, atr.Atr(14).atr(candles[-14:]))
            order.create_stop_loss(pair, atr.Atr(14).atr(candles[-14:]))
            
    
def maintain_trade(pair, strategy, candles):
    pair_info = order.get_order_info(pair)
    if int(pair_info['currentUnits']) < 0: # if short
        if strategy == 'long':
            order.close_trade(pair)
            order.long(pair, 1000)
    elif int(pair_info['currentUnits']) > 0: # if long
        if strategy == 'short':
            order.close_trade(pair)
            order.short(pair, 1000)
    return None

def check_exit(pair, candles):
    assert order.is_order_open(pair), f"{pair}, no pair to check exit for. {order.get_order_info}"
    escape = ssl.Ssl(25).cross_over(candles[-26:])
    pair_info = order.get_order_info(pair)
    if int(pair_info['currentUnits']) < 0: # if short
        if escape == 'long':
            order.close_trade(pair)
            print('ssl exit')
    elif int(pair_info['currentUnits']) > 0: # if long
        if escape == 'short':
            order.close_trade(pair)
            print('ssl exit')
    return None

def back_test(strategy, pair, count, granularity):
    candles = order.get_mid_candles(pair, count, granularity)
    return backtest.get_win_loss_ratio(strategy, candles)
    
def trade(strategy, pairs, **kwargs):
    print("finding trade entries...")
    for pair in pairs:
        candles = order.get_mid_candles(pair, 50, "M15")
        if not order.is_order_open(pair):
            find_trade(pair, strategy(candles), candles)
    print("maintaining trades...")
    for pair in order.get_open_orders():
        check_exit(pair, candles)
        if order.is_order_open(pair):
            maintain_trade(pair, strategy(candles), candles)

major_currencies = ["EUR_USD", "AUD_CAD", "AUD_CHF", "AUD_NZD", "AUD_USD", "CAD_CHF",
                    "EUR_AUD", "EUR_CAD", "EUR_CHF", "EUR_GBP", "EUR_NZD",
                    "GBP_AUD", "GBP_CAD", "GBP_CHF", "GBP_NZD", "GBP_USD", "NZD_CAD",
                    "USD_CAD", "USD_CHF", "USD_ZAR"]
trade(ssl.Ssl(6).which_trend, major_currencies)
#candles = order.get_mid_candles("EUR_USD", 50, "M15")
#find_trade("EUR_USD", strat.ma_crossover(candles), candles)

