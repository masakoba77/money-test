import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

DB_PATH = 'data/prices.db'

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            UNIQUE(symbol, date)
        )
    ''')
    conn.commit()
    conn.close()

def fetch_stock_data(symbol, start_date, end_date):
    """Fetch stock data from Yahoo Finance"""
    print(f"Fetching {symbol} data from {start_date} to {end_date}...")
    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    return data

def save_to_database(symbol, data):
    """Save stock data to SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for date, row in data.iterrows():
        date_str = date.strftime('%Y-%m-%d')
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO prices (symbol, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (symbol, date_str, row['Open'], row['High'], row['Low'], row['Close'], int(row['Volume'])))
        except Exception as e:
            print(f"Error inserting {symbol} {date_str}: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {len(data)} records for {symbol}")

def load_from_database(symbol, start_date=None, end_date=None):
    """Load stock data from SQLite"""
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT date, open, high, low, close, volume FROM prices WHERE symbol = '{symbol}'"

    if start_date:
        query += f" AND date >= '{start_date}'"
    if end_date:
        query += f" AND date <= '{end_date}'"

    query += " ORDER BY date ASC"

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return None

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

def fetch_and_save_stocks(symbols, start_date, end_date):
    """Fetch and save all stocks"""
    init_database()

    for symbol in symbols:
        try:
            data = fetch_stock_data(symbol, start_date, end_date)
            if not data.empty:
                save_to_database(symbol, data)
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
