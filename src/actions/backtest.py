def backtest(strategy, candles):
    """
    trade: {
        'order': {
            'open': True
            'position': 'long'
        }
        'entry': {
            'time': '2020-09-11T19:45:00.000000000Z',
            'price': 1.17783
        },
        'exit': {
            'time': '2020-09-13T19:45:00.000000000Z',
            'price': 1.17783
        },
        candles : [
            [1.18414, 1.18424, 1.18386, 1.18422],
            [1.18414, 1.18424, 1.18386, 1.18422],
            [1.18414, 1.18424, 1.18386, 1.18422]
        ]
    }
    """
    trades = []
    mid_candles = candles
    
    for i in range(len(mid_candles)-50): # all 50s are the candles needed for the indicator with the most candles needed for computation
        decision = strategy(mid_candles[i:50+i])
        if trades:
            if trades[-1]['order']['open']:
                if decision != trades[-1]['order']['position']: # if decision is opposite the order position, close the trade
                    trades[-1]['order']['open'] = False
                    trades[-1]['exit']['time'] = mid_candles[50+i]['time']
                    trades[-1]['exit']['price'] = mid_candles[50+i]['mid'][3] 
                    trades[-1]['candles'].append(mid_candles[50+i])
                else:
                    trades[-1]['candles'].append(mid_candles[50+i])
            else:
                trades.append({
                'order': {
                    'open': True,
                    'position': decision
                    },
                    'entry': {
                        'time': mid_candles[50+i]['time'],
                        'price': mid_candles[50+i]['mid'][3]
                    },
                    'exit': {
                        'time': None,
                        'price': None
                    },
                    'candles': [
                        mid_candles[50+i]
                    ]
                })
        else:
            trades.append({
                'order': {
                    'open': True,
                    'position': decision
                    },
                    'entry': {
                        'time': mid_candles[50+i]['time'],
                        'price': mid_candles[50+i]['mid'][3]
                    },
                    'exit': {
                        'time': None,
                        'price': None
                    },
                    'candles' : [
                        mid_candles[50+i]
                    ]
            })
    return trades
