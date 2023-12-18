import ta

def rsi(df_prices, window):
    df_prices['rsi'] = ta.momentum.rsi(df_prices.Close, window=window)
    df_prices.dropna(inplace=True)
    return df_prices
