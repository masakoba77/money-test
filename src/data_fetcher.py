import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_demo_data(days=250, symbol='AAPL'):
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    prices = []
    current_price = 150

    for i in range(days):
        change = np.random.normal(0.001, 0.02)
        current_price *= (1 + change)
        prices.append(current_price)

    data = {
        'date': dates,
        'open': [p * np.random.uniform(0.98, 1.02) for p in prices],
        'high': [p * np.random.uniform(1.00, 1.03) for p in prices],
        'low': [p * np.random.uniform(0.97, 1.00) for p in prices],
        'close': prices,
        'volume': [np.random.randint(1000000, 10000000) for _ in range(days)]
    }

    df = pd.DataFrame(data)
    return df

def fetch_data(symbol, start_date=None, end_date=None):
    try:
        import yfinance as yf

        if start_date is None:
            start_date = datetime.now() - timedelta(days=250)
        if end_date is None:
            end_date = datetime.now()

        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)

        if df is None or len(df) == 0:
            return generate_demo_data()

        df = df.reset_index()
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'splits']
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

        return df
    except:
        return generate_demo_data()
