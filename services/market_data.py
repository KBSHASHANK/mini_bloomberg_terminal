import yfinance as yf
import pandas as pd
import requests

def get_historical_data(symbol: str) -> pd.DataFrame:
    symbol = symbol.strip().upper()
    
    # Create a custom session with a browser User-Agent to avoid getting blocked by Yahoo Finance
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    stock = yf.Ticker(symbol, session=session)
    data = stock.history(period="1y")
    
    return data