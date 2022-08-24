import pandas as pd
import numpy as np

def bittrex_order(raw):
    df = pd.DataFrame()
    df['Date and Time'] = pd.to_datetime(raw['OPENED']).dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    raw['ORDER'] = raw['ORDERTYPE'].str.split('_', expand=True)[1]

    conditions = [
        (raw['ORDER'] == 'BUY') & (raw['MARKET'] == 'USD'),
        (raw['ORDER'] == 'SELL') & (raw['MARKET'] == 'USD'),
        raw['MARKET'] != 'USD'
    ]

    values = ['BUY', 'SELL', 'TRADE']
    df["Transaction Type"] = np.select(conditions, values)

    df.loc[raw['ORDER'] == 'SELL', 'Sent Quantity'] = raw['FILLED']
    df.loc[raw['ORDER'] == 'BUY', 'Sent Quantity'] = raw['PROCEEDS']

    df.loc[raw['ORDER'] == 'SELL', 'Sent Currency'] = raw['QUOTE']
    df.loc[raw['ORDER'] == 'BUY', 'Sent Currency'] = raw['MARKET']

    df['Sending Source'] = 'Bittrex'

    df.loc[raw['ORDER'] == 'SELL', 'Received Quantity'] = raw['PROCEEDS']
    df.loc[raw['ORDER'] == 'BUY', 'Received Quantity'] = raw['FILLED']

    df.loc[raw['ORDER'] == 'SELL', 'Sent Currency'] = raw['MARKET']
    df.loc[raw['ORDER'] == 'BUY', 'Sent Currency'] = raw['QUOTE']

    df['Receiving Destination'] = 'Bittrex'

    df['Fee'] = raw['COMISSIONPAID']

    df['Fee Currency'] = raw['MARKET']

    df['Exchange Transaction ID'] = None

    df['Blockchain Transaction Hash'] = None

    return df