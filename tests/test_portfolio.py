from services.database import init_db
from services.portfolio import add_stock, load_portfolio

init_db()

add_stock("AAPL", 10, 180)

df = load_portfolio()

print(df)