import numpy as np
import pandas as pd


def strategy(df_prices, rsi_lower: float, rsi_upper: float, stop_loss: bool, sl=0):
    conditions = [(df_prices.rsi < rsi_upper) & (df_prices.Close < df_prices.lower_bb),
                  (df_prices.rsi > rsi_lower) & (df_prices.Close > df_prices.upper_bb)]
    choices = ['Buy', 'Sell']

    df_prices['signal'] = np.select(conditions, choices)
    df_prices.dropna(inplace=True)

    df_prices.signal = df_prices.signal.shift()
    df_prices['shifted_Close'] = df_prices.Close.shift()

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for index, row in df_prices.iterrows():
        if not position and row['signal'] == 'Buy':
            buydates.append(index)
            buyprices.append(row.Open)
            position = True

        if position:
            if stop_loss:
                if row['signal'] == 'Sell' or row.shifted_Close < sl * buyprices[-1]:
                    selldates.append(index)
                    sellprices.append(row.Open)
                    position = False
            else:
                if row['signal'] == 'Sell':
                    selldates.append(index)
                    sellprices.append(row.Open)
                    position = False

    rtn = (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1
    buy = pd.DataFrame({'buydate': buydates,
                         'buyprices':buyprices})
    sell = pd.DataFrame({'selldate': selldates,
                         'sellprices':sellprices})
    output = {'df': df_prices,
              'buy': buy,
              'sell': sell,
              'buydates': buydates,
              'buyprices': buyprices,
              'selldates': selldates,
              'sellprices': sellprices,
              'return': rtn}
    return output
