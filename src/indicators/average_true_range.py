# take in an array of 14 rows and 4 columns.
class Atr:
    def __init__(self, period):
        self.period = period

    def atr(self, array):
        """ Measures market volatility.

        How to read: 0.0003 is 3 pips, 0.01 is 1 pip for JPY

        Formula (according to Investopedia):
            Average True Range = sum(True Range) / period
            True Range (per candle) = Max[(high - low), Abs(high - close), Abs(low - close)]

        Args:
            array: a list of [open,high,low,close] candles, where the length
                of the array corresponds to the period.
        
        Returns: 
            an Integer representing the ATR in pips.
        """
        assert len(array) >= self.period, f"length of array for Atr.atr() is too small, size {len(array)}. Must be at least {self.period}"
        candles = array[-self.period:]
        tr_sum = 0
        for i in range(len(candles)):
            tr_sum += max(abs(candles[i]['mid'][1] - candles[i]['mid'][2]),
                        abs(candles[i]['mid'][1] - candles[i]['mid'][3]), 
                        abs(candles[i]['mid'][2] - candles[i]['mid'][3]))
        atr = tr_sum / len(candles)
        return atr  