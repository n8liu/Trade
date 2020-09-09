import order
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def candlestick_chart(pair, count, granularity):
    candles = order.get_candles(pair, count, granularity, 'M')
    fig = go.Figure(data=[go.Candlestick(
                                x=[candle[5] for candle in candles],
                                open=[candle[0] for candle in candles],
                                high=[candle[1] for candle in candles],
                                low=[candle[2] for candle in candles],
                                close=[candle[3] for candle in candles])
    ])
    fig.show()

def cross_over(ma, pair, count, granularity):
    candles = order.get_candles(pair, count, granularity, 'M')
    data = generate_crossover_data(3, candles)
    
    fig = go.Figure(data=[go.Scatter(
        x=[elem['x'] for elem in data],
        y=[elem['y'] for elem in data]
    )])
    fig.show()

def strategy1(pair, count, granularity):
    assert count > 51, "need more than 50 candles to run strategy chart"
    candles = order.get_candles(pair, count, granularity, 'M')
    data_fast = generate_crossover_data(9, candles)
    data_slow = generate_crossover_data(50, candles)

    fig = make_subplots(
        rows=1, cols=1,
        shared_xaxes=True
    )

    fig.add_trace(
        go.Scatter(
            x=[elem['x'] for elem in data_fast],
            y=[elem['y'] for elem in data_fast],
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[elem['x'] for elem in data_slow],
            y=[elem['y'] for elem in data_slow],
        )
    )
    fig.add_trace(
        go.Candlestick(
            x=[candle[5] for candle in candles],
            open=[candle[0] for candle in candles],
            high=[candle[1] for candle in candles],
            low=[candle[2] for candle in candles],
            close=[candle[3] for candle in candles]
        )
    )
    fig.show()


def generate_crossover_data(ma, candles):
        data = []
        for i in range(len(candles)-ma):
            data.append({'x': candles[ma+i][5],
                        'y': sum(candle[3] for candle in candles[i:ma+i]) / ma})
        return data

strategy1("EUR_USD", 500, "M15")