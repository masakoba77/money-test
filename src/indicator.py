import pandas as pd
import numpy as np

class PriceData:
    def __init__(self, date, open_price, high, low, close, volume):
        self.date = date
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.sma20 = None
        self.sma50 = None
        self.rsi = None
        self.signal = None

def calculate_sma(prices, period):
    return pd.Series(prices).rolling(window=period).mean().values

def calculate_rsi(prices, period=14):
    series = pd.Series(prices)
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.values

def add_indicators(df):
    if df is None or len(df) == 0:
        return df

    prices = df['close'].values
    df['sma20'] = calculate_sma(prices, 20)
    df['sma50'] = calculate_sma(prices, 50)
    df['rsi'] = calculate_rsi(prices, 14)
    return df

def get_crossover_signal(sma20, sma50, prev_sma20, prev_sma50):
    if sma20 is None or sma50 is None or prev_sma20 is None or prev_sma50 is None:
        return 'HOLD'
    if prev_sma20 <= prev_sma50 and sma20 > sma50:
        return 'GOLDEN_CROSS'
    if prev_sma20 >= prev_sma50 and sma20 < sma50:
        return 'DEATH_CROSS'
    return 'HOLD'

def assign_signals(df):
    if df is None or len(df) < 2:
        return df

    df['signal'] = 'HOLD'
    for i in range(1, len(df)):
        prev_row = df.iloc[i-1]
        curr_row = df.iloc[i]
        signal = get_crossover_signal(
            curr_row.get('sma20'),
            curr_row.get('sma50'),
            prev_row.get('sma20'),
            prev_row.get('sma50')
        )
        df.at[df.index[i], 'signal'] = signal

    return df
