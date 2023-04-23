import pandas as pd

def Performance_calculator(buyprices, sellprices):
    rtn = (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices, buyprices)]) + 1).prod() - 1
    return round(rtn * 100, 2)