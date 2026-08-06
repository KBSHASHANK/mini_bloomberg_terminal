import pandas as pd
from services.database import get_connection


def add_stock(
    ticker: str,
    shares: float,
    buy_price: float,
    purchase_date: str
):
    """
    Add a stock to the portfolio.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO portfolio
        (ticker, shares, buy_price, purchase_date)
        VALUES (?, ?, ?, ?)
    """, (
        ticker.upper(),
        shares,
        buy_price,
        purchase_date
    ))

    conn.commit()
    conn.close()


def load_portfolio() -> pd.DataFrame:
    """
    Load the entire portfolio.
    """

    conn = get_connection()

    df = pd.read_sql("""
        SELECT *
        FROM portfolio
        ORDER BY purchase_date DESC
    """, conn)

    conn.close()

    return df


def delete_stock(stock_id: int):
    """
    Delete a stock from the portfolio.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM portfolio WHERE id = ?",
        (stock_id,)
    )

    conn.commit()
    conn.close()