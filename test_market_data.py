from services.market_data import get_historical_data


data = get_historical_data("AAPL")

print(data.head())
print()
print(data.tail())
print()
print(data.columns)