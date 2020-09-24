from actions import backtest
from actions import graph
from actions import order
from strategy import moving_avg_cross_over as ma
from strategy import ssl_cross_over
from strategy.indicators import ssl
from strategy.indicators import moving_averages

candles = order.get_mid_candles("EUR_USD", 30, "M15")
#strat = ssl.generate_ssl_data(candles, 25)

#graph.create_strategy_chart(candles, backtest.backtest(ssl_cross_over.cross_over, candles), up=strat['up'], down=strat['down'])

#backtest.get_win_loss_ratio(ssl_cross_over.cross_over, candles)

confirmation = ssl.Ssl(25)
ma = moving_averages.SimpleMovingAverage(25)
#print(confirmation.which_trend(candles))
#print(confirmation.generate_data(candles))
print(ma.generate_data(candles))