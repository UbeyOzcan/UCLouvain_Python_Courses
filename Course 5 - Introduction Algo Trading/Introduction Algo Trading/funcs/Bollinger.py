import pandas as pd

def bollinger(df_prices:pd.DataFrame, window: int, delta: float):

    df_prices[f"ma_n"] = df_prices.Close.rolling(window).mean()
    df_prices['vol'] = df_prices.Close.rolling(window).std()
    df_prices['upper_bb'] = df_prices[f"ma_n"] + (delta * df_prices.vol)
    df_prices['lower_bb'] = df_prices[f"ma_n"] - (delta * df_prices.vol)

    df_prices.dropna(inplace=True)
    return df_prices