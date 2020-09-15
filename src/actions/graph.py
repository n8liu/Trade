from . import order
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def candlestick_chart(pair, count, granularity):
    candles = order.get_candles(pair, count, granularity, 'M')
    fig = go.Figure(data=[go.Candlestick(
                                x=[candle['time'] for candle in candles],
                                open=[candle['mid'][0] for candle in candles],
                                high=[candle['mid'][1] for candle in candles],
                                low=[candle['mid'][2] for candle in candles],
                                close=[candle['mid'][3] for candle in candles])
    ])
    fig.show()

def trade_timeline(candles):
    fig = go.Figure(data=[go.Candlestick(
                                x=[candle['time'] for candle in candles],
                                open=[candle['mid'][0] for candle in candles],
                                high=[candle['mid'][1] for candle in candles],
                                low=[candle['mid'][2] for candle in candles],
                                close=[candle['mid'][3] for candle in candles])
    ])
    fig.show()

def create_strategy_chart(candles, **kwargs):
    """ shows a figure

    args:
    **kwargs: must be a list of dictionaries {'x': , 'y':} where x is a datetime and 
    y is indicator data. Indicators with many y points for each x must be split into
    different kwargs
    """
    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True
    )
    fig.add_trace(
        go.Candlestick(
            x=[candle['time'] for candle in candles],
            open=[candle['mid'][0] for candle in candles],
            high=[candle['mid'][1] for candle in candles],
            low=[candle['mid'][2] for candle in candles],
            close=[candle['mid'][3] for candle in candles]
        )
    )
    for key, indicator in kwargs.items():
        fig.add_trace(
            go.Scatter(
                x=[elem['x'] for elem in indicator],
                y=[elem['y'] for elem in indicator],
                name=key
            )
        )
    fig.show()

def show_fig():
    candles = order.get_candles("EUR_USD", 500, 'M15', 'M')
    ma_9 = generate_crossover_data(9, candles)
    ma_50 = generate_crossover_data(50, candles)
    ma_200 = generate_crossover_data(200, candles)

    create_strategy_chart(ma_9=ma_9, ma_50=ma_50, ma_200=ma_200)

def generate_crossover_data(ma, candles):
    data = []
    for i in range(len(candles)-ma):
        data.append({'x': candles[ma+i]['time'],
                    'y': sum(candle['mid'][3] for candle in candles[i:ma+i]) / ma})
    return data
