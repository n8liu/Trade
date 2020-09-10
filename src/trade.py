from strategy import moving_avg_cross_over as strat
from actions import order

def find_trades():
    candles = order.get_candles("EUR_USD", 51, "M5")
    decision = strat.ma_crossover(candles)
    if decision == 'long':
        order.long("EUR_USD", 1000)
    elif decision == 'short':
        order.short("EUR_USD", 1000)
    else:
        order.long("EUR_USD", 1000)

def trade():
    if not order.is_order_open("EUR_USD"):
        find_trades()

trades()