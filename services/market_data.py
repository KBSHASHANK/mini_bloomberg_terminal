import yfinance as yf
import pandas as pd


def get_historical_data(symbol):
    symbol = symbol.strip().upper()

    stock = yf.Ticker(symbol)

    data = stock.history(period="1y")

    return data