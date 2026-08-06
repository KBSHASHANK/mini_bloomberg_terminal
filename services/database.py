
import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "market_data.db")

def get_connection():
    """Ensure the data directory exists and return a SQLite connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for historical OHLCV data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            UNIQUE(ticker, date)
        )
    """)
    
    conn.commit()
    conn.close()

def save_historical_data(ticker: str, df: pd.DataFrame):
    """Save or update historical price DataFrame into SQLite."""
    if df.empty:
        return
    
    conn = get_connection()
    
    # Format DataFrame for database insertion
    df_to_save = df.copy()
    df_to_save.reset_index(inplace=True)
    
    # Normalize column names depending on yfinance structure (handle MultiIndex or standard)
    if 'Date' in df_to_save.columns:
        df_to_save['date'] = pd.to_datetime(df_to_save['Date']).dt.strftime('%Y-%m-%d')
    elif 'Datetime' in df_to_save.columns:
        df_to_save['date'] = pd.to_datetime(df_to_save['Datetime']).dt.strftime('%Y-%m-%d')
        
    df_to_save['ticker'] = ticker.upper()
    
    # Map common columns
    col_mapping = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}
    df_to_save.rename(columns=col_mapping, inplace=True)
    
    required_cols = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
    existing_cols = [c for c in required_cols if c in df_to_save.columns]
    
    # Insert or Replace into database to avoid duplicates
    temp_records = df_to_save[existing_cols].to_dict(orient='records')
    cursor = conn.cursor()
    
    for row in temp_records:
        cursor.execute("""
            INSERT OR REPLACE INTO historical_prices (ticker, date, open, high, low, close, volume)
            VALUES (:ticker, :date, :open, :high, :low, :close, :volume)
        """, row)
        
    conn.commit()
    conn.close()

def load_historical_data(ticker: str) -> pd.DataFrame:
    """Load historical data from SQLite for a given ticker."""
    conn = get_connection()
    query = "SELECT date, open, high, low, close, volume FROM historical_prices WHERE ticker = ? ORDER BY date ASC"
    df = pd.read_sql(query, conn, params=(ticker.upper(),))
    conn.close()
    
    if not df.empty:
        # Capitalize columns to match app.py expectations ('Close', 'High', etc.)
        df.columns = [col.capitalize() for col in df.columns]
        
        # Ensure index is set correctly as datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
    return df