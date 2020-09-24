""" SSL indicator lives here.

SSL is a confirmation and exit indicator. An explanation for this indicator 
doesn't really exist...

The calculation for this indicator is a complete mystery.
"""
from . import sma

class Ssl:
    """ class for the ssl channel chart indicator.
    example:
    Ssl(25) is the indicator with a period of 25 candles
    """
    def __init__(self, period):
        self.period = period
    
    def ssl(self, candles):
        '''Returns the SSL of an array.
        this function is a utility function and should only be called be other functions
        in this class.

        args:
        candles: a list of candles
        '''
        hlv_array = [0 for candles in range(len(candles))]

        for i in range(len(candles)):
            sma_h = sma.SimpleMovingAverage(self.period).high(candles)
            sma_l = sma.SimpleMovingAverage(self.period).low(candles)
            
            if i == 0:
                hlv_array[1] = hlv_array[0]
            else:
                hlv_array[i] = hlv_array[i-1]
        
            if candles[i]['mid'][3] > sma_h:
                hlv_array[i] = 1
            elif candles[i]['mid'][3] < sma_l:
                hlv_array[i] = -1
            
        ssl_up = sma_l if hlv_array[-1] < 0 else sma_h
        ssl_down = sma_h if hlv_array[-1] < 0 else sma_l

        return [ssl_up, ssl_down]
    
    def generate_data(self, candles):
        """ return data for graphing purposes, or any activity requiring more than one
        data point.

        args:
        candles: a list of candles.

        returns:
        a dictionary containing a list of dictionaries {'up': {'x': datetime, 'y': float}, 'down': {'x': datetime, 'y': float}, 
        where up is ssl channel chart up line, and down is the ssl down line. each x is a datetime, and each y is a point 
        ssl line data. Each list is size ssl period - candle length.

        ex:
        Ssl(25).generate_data(order.get_mid_candles("EUR_USD", 30, "M15"))
        {'up': [{'x': '2020-09-23T21:30:00.000000000Z', 'y': 1.1666972000000002}, 
                {'x': '2020-09-23T21:45:00.000000000Z', 'y': 1.1666332}, 
                {'x': '2020-09-23T22:00:00.000000000Z', 'y': 1.1665903999999998}, 
                {'x': '2020-09-23T22:15:00.000000000Z', 'y': 1.1665631999999997}, 
                {'x': '2020-09-23T22:30:00.000000000Z', 'y': 1.1665168}], 
        'down': [{'x': '2020-09-23T21:30:00.000000000Z', 'y': 1.1673904000000004}, 
                 {'x': '2020-09-23T21:45:00.000000000Z', 'y': 1.1672888000000001}, 
                 {'x': '2020-09-23T22:00:00.000000000Z', 'y': 1.1672200000000001}, 
                 {'x': '2020-09-23T22:15:00.000000000Z', 'y': 1.1671620000000003}, 
                 {'x': '2020-09-23T22:30:00.000000000Z', 'y': 1.1670848000000003}]}
        """
        ssl_up = []
        ssl_down = []
        for i in range(len(candles)-self.period):
            ssl_up.append({'x': candles[i+self.period]['time'], 'y': self.ssl(candles[i:i+self.period])[0]})
            ssl_down.append({'x': candles[i+self.period]['time'], 'y': self.ssl(candles[i:i+self.period])[1]})
        return {'up': ssl_up, 'down': ssl_down}
    
    # ways to interpret ssl data
    def which_trend(self, candles):
        """ provide signal based on which ssl line is higher. If ssl 'up' is higher, returns long signal. If 
        ssl 'down' is higher, returns a short signal. Otherwise it waits.
        
        args:
        candles: a list of candles that must be greater than or equal to the period
        """
        assert len(candles) >= self.period, (f"too few candles given to calculate which trend. Must be {self.period}, {len(candles)} were given.")
        ssl_data = self.ssl(candles[-self.period:]) # [up, down]
        if ssl_data[0] > ssl_data[1]:
            return 'long'
        elif ssl_data[0] < ssl_data[1]:
            return 'short'
        return 'wait'
    
    def cross_over(self, candles):
        """ Porvides a long/short signal based on when ssl 'up' and ssl 'down' cross over one another.

        args:
        candles: a list of candles
        """
        assert len(candles) == self.period + 1, f"To calculate Ssl().cross_over, {self.period+1} candles are needed. {len(candles)} were given."
        now = self.which_trend(candles[1:])
        previous =  self.which_trend(candles[:-1])
        if now == 'long' and previous == 'short':
            return 'long'
        elif now == 'short' and previous == 'long':
            return 'short'
        else:
            return 'wait'