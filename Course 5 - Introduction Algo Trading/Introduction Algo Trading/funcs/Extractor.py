import yfinance as yf

def extract_stock_price(ticker: str, start: str, end: str):
    df = yf.download(ticker,
                     start=start,
                     end=end)

    return df
