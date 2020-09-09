import requests
import json
from decouple import config

account_number = config('ACCOUNT_NUMBER')
practice_trade_token = config('PRACTICE_TRADE_TOKEN')

header = {
    'Content-Type': 'application/json',
    'Authorization': practice_trade_token, # change this to live when in production
}

def long(currency_pair, order_size):
    """ executes a short order using Oanda API

    Args:
        currency_pair: a string, must be all caps like "EUR_USD". convert a currency pair you'd see
        like EUR/USD or USD/JPY to EUR_USD or USD_JPY respectively.
        order_size: an integer, the number of units of the currency pair to be ordered
    
    Returns:
        An integer representing the HTTP status code of the API call
    """
    params = {
        "order": {
            "stopLossOnFill": {
            "price": "1.7000"
            },
            "takeProfitOnFill": {
            "price": "1.14530"
            },
            "units": str(order_size),
            "instrument": currency_pair,
            "timeInForce": "IOC",
            "type": "MARKET",
            "positionFill": "DEFAULT",
        }
    }
    response = requests.post(f'https://api-fxpractice.oanda.com/v3/accounts/{account_number}/orders', 
                            headers=header, data=json.dumps(params))
    print('long', response.status_code)
    return response.status_code

def short(currency_pair, order_size):
    """ executes a short order using Oanda API

    Args:
        currency_pair: a string, must be all caps like "EUR_USD". convert a currency pair you'd see
        like EUR/USD or USD/JPY to EUR_USD or USD_JPY respectively.
        order_size: order_size: an integer, the number of units of the currency pair to be ordered
    
    Returns:
        An integer, the HTTP status code of the API call
    """
    params = {
        "order": {
            "stopLossOnFill": {
            "price": "1.7000"
            },
            "takeProfitOnFill": {
            "price": "1.14530"
            },
            "units": "-" + str(order_size),
            "instrument": currency_pair,
            "timeInForce": "IOC",
            "type": "MARKET",
            "positionFill": "DEFAULT",
        }
    }
    response = requests.post('https://api-fxpractice.oanda.com/v3/accounts/101-001-11802828-001/orders', 
                            headers=header, data=json.dumps(params))
    print('short', response.status_code)
    return response.status_code

def get_candles(pair, count, granularity, price='M'):
    """ Returns candles that are ready to be used in calculations

    args:
        pair: string; "ABC_XYZ" for which pair we should get data from.
        count: integer, number of candles to return
        granularity: string. Time frame of the candles, ('S5', 'M1', 'M5', 'M15', 'M30', 'H1-H4', 
        'H6', 'H8', 'H12', 'D', 'W')
        price: which candles are returned, either bid candles, ask candles, or midpoint of both.
        ('B', 'A', 'BA', or 'M')
    
    returns:
        a list of candles
    """
    data = (
        ('count', str(count)),
        ('price', price),
        ('granularity', granularity),
    )

    response = requests.get(f"https://api-fxpractice.oanda.com/v3/instruments/{pair}/candles", 
                                    headers=header, params=data)
    parsed_response = json.loads(response.text)
    
    if response.status_code != 200: # throw error if GET doesn't go through
        raise Exception(ValueError, f"status code is not 200, but {response.status_code} at {pair}")
    candles = []
    for i in range(int(data[0][1])): # iterate through the number of candles we got.
        next_bid = [float(parsed_response['candles'][i]['mid']['o']), 
                    float(parsed_response['candles'][i]['mid']['h']),
                    float(parsed_response['candles'][i]['mid']['l']),
                    float(parsed_response['candles'][i]['mid']['c']),
                    float(parsed_response['candles'][i]['volume']),
                    parsed_response['candles'][i]['time']]
        candles += [next_bid]
    return candles

def is_order_open(pair):
    """ returns True if there's an open order for the given pair,
    False if there isn't an open order for the given pair

    args:
    pair: a string, must be all caps like "EUR_USD". convert a currency pair you'd see
        like EUR/USD or USD/JPY to EUR_USD or USD_JPY respectively.
    
    returns:
    a boolean, True if an open order in the given pair exists, False otherwise.
    """
    response = requests.get(f"https://api-fxpractice.oanda.com/v3/accounts/{account_number}/openTrades", 
                                    headers=header)
    parsed_response = json.loads(response.text)
    
    if parsed_response['trades']:
        for trade in parsed_response['trades']:
            if trade['instrument'] == pair:
                return True
    return False