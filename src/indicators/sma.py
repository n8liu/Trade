class SimpleMovingAverage:
    """ class for the moving average indicator.

    example:

    SimpleMovingAverage(25).
    """
    def __init__(self, period):
        self.period = period
    
    """ moving average lines:
    thses three functions compute a single point using either the high, low, or close
    of a list of candles. 
    """
    def close(self, candles):
        return sum([candle['mid'][3] for candle in candles]) / len(candles)
    
    def low(self, candles):
        return sum([candle['mid'][2] for candle in candles]) / len(candles)
    
    def high(self, candles):
        return sum([candle['mid'][1] for candle in candles]) / len(candles)

    def generate_data(self, candles):
        """ return data for graphing purposes, or any activity requiring more than one
        data point, like other functions that use ma data for computation.

        args:
        candles: a list of candles.

        returns:
        a list of dictionaries {'x': datetime, 'y': float}, Where 'y' is a list of moving average points, and
        'x' is a list of datetimes.

        ex:
        SimpleMovingAverage(25).generate_data(order.get_mid_candles("EUR_USD", 30, "M15"))
        [{'x': '2020-09-23T22:15:00.000000000Z', 'y': 1.166824}, 
         {'x': '2020-09-23T22:30:00.000000000Z', 'y': 1.1667636000000001}, 
         {'x': '2020-09-23T22:45:00.000000000Z', 'y': 1.1666800000000002}, 
         {'x': '2020-09-23T23:00:00.000000000Z', 'y': 1.1665708}, 
         {'x': '2020-09-23T23:15:00.000000000Z', 'y': 1.1664836}]
        """
        data = []
        for i in range(len(candles)-self.period):
            data.append({'x': candles[self.period+i]['time'],
                         'y': sum(candle['mid'][3] for candle in candles[i:self.period+i]) / self.period})
        return data
    
    # ways to read moving average data
    def which_trend(self, candles):
        """ baseline indicator read: if price is higher than the moving average,
        it's an uptrend, if price is below the moving average, it's a downtrend.

        args:
        candles: a list of candles
        """
        if candles[-1]['mid'][3] > self.close(candles):
            return 'long'
        elif candles[-1]['mid'][3] < self.close(candles):
            return 'short'
        else:
            return 'wait'
