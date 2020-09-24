import requests
import json
from decouple import config

account_number = config('ACCOUNT_NUMBER')
practice_trade_token = config('PRACTICE_TRADE_TOKEN')

header = {
    'Content-Type': 'application/json',
    'Authorization': practice_trade_token, # change this to live when in production
}

#####################################################################################################
# Candles                                                                                           #
#####################################################################################################
def get_mid_candles(pair, count, granularity):
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
        ('price', 'M'),
        ('granularity', granularity),
    )

    response = requests.get(f"https://api-fxpractice.oanda.com/v3/instruments/{pair}/candles", 
                                    headers=header, params=data)
    parsed_response = json.loads(response.text)
    
    if response.status_code != 200: # throw error if GET doesn't go through
        raise Exception(ValueError, f"status code is not 200, but {response.status_code} at {pair}")
    candles = []
    for i in range(int(data[0][1])): # iterate through the number of candles we got.
        next_mid = {'mid': [float(parsed_response['candles'][i]['mid']['o']), 
                            float(parsed_response['candles'][i]['mid']['h']),
                            float(parsed_response['candles'][i]['mid']['l']),
                            float(parsed_response['candles'][i]['mid']['c'])],
                    'volume': float(parsed_response['candles'][i]['volume']),
                    'time': parsed_response['candles'][i]['time']}
        candles += [next_mid]
    return candles

def get_ba_candles(pair, count, granularity):
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
        ('price', 'BA'),
        ('granularity', granularity),
    )

    response = requests.get(f"https://api-fxpractice.oanda.com/v3/instruments/{pair}/candles", 
                                    headers=header, params=data)
    parsed_response = json.loads(response.text)
    
    if response.status_code != 200: # throw error if GET doesn't go through
        raise Exception(ValueError, f"status code is not 200, but {response.status_code} at {pair}")
    candles = []
    for i in range(int(data[0][1])): # iterate through the number of candles we got.
        next_candle = {'bid': [float(parsed_response['candles'][i]['bid']['o']), 
                            float(parsed_response['candles'][i]['bid']['h']),
                            float(parsed_response['candles'][i]['bid']['l']),
                            float(parsed_response['candles'][i]['bid']['c'])],
                        'ask': [float(parsed_response['candles'][i]['ask']['o']), 
                            float(parsed_response['candles'][i]['ask']['h']),
                            float(parsed_response['candles'][i]['ask']['l']),
                            float(parsed_response['candles'][i]['ask']['c'])],
                        'volume': float(parsed_response['candles'][i]['volume']),
                        'time': parsed_response['candles'][i]['time']}
        candles += [next_candle]
    return candles

#####################################################################################################
# Trades - Get Details on Current Positions                                                         #
#####################################################################################################
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

def get_order_info(pair):
    """ returns:
    {'id': '7190', 
    'instrument': 'EUR_USD', 'price': '1.18501', 
    'openTime': '2020-09-15T17:25:28.523607972Z', 'initialUnits': '-1000', 
    'initialMarginRequired': '23.7016', 'state': 'OPEN', 
    'currentUnits': '-1000', 
    'realizedPL': '0.0000', 'financing': '0.0000', 'dividendAdjustment': '0.0000', 
    'unrealizedPL': '-0.0600', 'marginUsed': '23.7002'}
    """
    response = requests.get(f"https://api-fxpractice.oanda.com/v3/accounts/{account_number}/openTrades", 
                                    headers=header)
    parsed_response = json.loads(response.text)
    
    if parsed_response['trades']:
        for trade in parsed_response['trades']:
            if trade['instrument'] == pair:
                return trade
        print('order pair:', pair, trade)
    
    return f'could not find {pair} using get_order_info().'

def get_open_orders():
    """ returns a list of current open orders
    """
    open_orders = []
    response = requests.get(f"https://api-fxpractice.oanda.com/v3/accounts/{account_number}/openTrades", 
                                    headers=header)
    parsed_response = json.loads(response.text)
    
    if parsed_response['trades']:
        for trade in parsed_response['trades']:
            open_orders.append(trade['instrument'])
    return open_orders


#####################################################################################################
# Order - Create Orders and Modify Trades                                                           #
#####################################################################################################
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
            "units": str(order_size),
            "instrument": currency_pair,
            "timeInForce": "IOC",
            "type": "MARKET",
            "positionFill": "DEFAULT",
        }
    }
    response = requests.post(f"https://api-fxpractice.oanda.com/v3/accounts/{account_number}/orders", 
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
            "units": "-" + str(order_size),
            "instrument": currency_pair,
            "timeInForce": "IOC",
            "type": "MARKET",
            "positionFill": "DEFAULT",
        }
    }
    response = requests.post(f'https://api-fxpractice.oanda.com/v3/accounts/{account_number}/orders', 
                            headers=header, data=json.dumps(params))
    print('short', response.status_code)
    return response.status_code

def create_take_profit(pair, distance):
    """
    """
    trade = get_order_info(pair)
    print('distance', distance)
    print(trade['currentUnits'])
    #print('current units', int(trade['currentUnits']))
    if int(trade['currentUnits']) < 0: # if trade is short
        price = float(trade['price']) - 1.0 * distance
    elif int(trade['currentUnits']) > 0: # if trade is long
        price = float(trade['price']) + 1.0 * distance
    
    print('take_profit:', str(price)[:6])
    params = {
        "order": {
            "timeInForce": "GTC",
            "price": str(price)[:6],
            "type": "TAKE_PROFIT",
            "tradeID": trade['id']
        }
    }
    response = requests.post(f'https://api-fxpractice.oanda.com/v3/accounts/{account_number}/orders', 
                            headers=header, data=json.dumps(params))
    print('take profit', response.status_code)
    return response.status_code

def create_stop_loss(pair, distance):
    """
    """
    trade = get_order_info(pair)
    print('distance', distance)
    print('current units', int(trade['currentUnits']))
    if int(trade['currentUnits']) < 0: # if trade is short
        price = float(trade['price']) + 1.0 * distance
    elif int(trade['currentUnits']) > 0: # if trade is long
        price = float(trade['price']) - 1.0 * distance
    print('take_profit:', str(price)[:6])
    params = {
        "order": {
            "timeInForce": "GTC",
            "price": str(price)[:6],
            "type": "STOP_LOSS",
            "tradeID": trade['id']
        }
    }
    response = requests.post(f'https://api-fxpractice.oanda.com/v3/accounts/{account_number}/orders', 
                            headers=header, data=json.dumps(params))
    print('stop loss', response.status_code)
    return response.status_code

def close_trade(pair):
    """
    """
    info = get_order_info(pair)
    if int(info['currentUnits']) < 0: # if short
        params = {
            "longUnits": "ALL"
        }
    else:
        params = {
            "shortUnits": "ALL"
        }
    response = requests.put(f'https://api-fxpractice.oanda.com/v3/accounts/{account_number}/positions/{pair}/close', 
                            headers=header, data=json.dumps(params))
    print(pair,' trade closed', response.status_code)
    return response.status_code
