import yfinance as yf
import numpy as np
import ta


def Strategy_1(ticker, start, end, bb_period, rsi_period, stop_loss=False, SL=0):
    df = yf.download(ticker, start=start, end=end)
    df['ma_20'] = df.Close.rolling(bb_period).mean()
    df['vol'] = df.Close.rolling(bb_period).std()
    df['upper_bb'] = df.ma_20 + (2 * df.vol)
    df['lower_bb'] = df.ma_20 - (2 * df.vol)
    df['rsi'] = ta.momentum.rsi(df.Close, window=rsi_period)

    conditions = [(df.rsi < 300) & (df.Close < df.lower_bb),
                  (df.rsi > 70) & (df.Close > df.upper_bb)]
    choices = ['Buy', 'Sell']

    df['signal'] = np.select(conditions, choices)
    df.dropna(inplace=True)

    df.signal = df.signal.shift()
    df['shifted_Close'] = df.Close.shift()

    position = False
    buydates, selldates = [], []
    buyprices, sellprices = [], []

    for index, row in df.iterrows():
        if not position and row['signal'] == 'Buy':
            buydates.append(index)
            buyprices.append(row.Open)
            position = True

        if position:
            if stop_loss:
                if row['signal'] == 'Sell' or row.shifted_Close < SL * buyprices[-1]:
                    selldates.append(index)
                    sellprices.append(row.Open)
                    position = False
            else:
                if row['signal'] == 'Sell':
                    selldates.append(index)
                    sellprices.append(row.Open)
                    position = False

    output = {'df': df,
              'buydates': buydates,
              'buyprices': buyprices,
              'selldates': selldates,
              'sellprices': sellprices}
    return output