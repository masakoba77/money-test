import pandas as pd
import numpy as np

def calculate_sma(data, period):
    """Calculate Simple Moving Average"""
    close_col = 'close' if 'close' in data.columns else 'Close'
    return data[close_col].rolling(window=period).mean()

def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index"""
    close_col = 'close' if 'close' in data.columns else 'Close'
    delta = data[close_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_indicators(data, short_ma=20, long_ma=50):
    """Add technical indicators to data"""
    df = data.copy()
    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()
    df['sma_short'] = calculate_sma(df, short_ma)
    df['sma_long'] = calculate_sma(df, long_ma)
    df['rsi'] = calculate_rsi(df)
    return df

def get_crossover_signal(data):
    """Generate buy/sell signals based on MA crossover
    Returns: 1 for buy signal, -1 for sell signal, 0 for hold
    """
    signals = []

    for i in range(1, len(data)):
        prev_short = data.iloc[i-1]['sma_short']
        prev_long = data.iloc[i-1]['sma_long']
        curr_short = data.iloc[i]['sma_short']
        curr_long = data.iloc[i]['sma_long']

        # Skip if NaN
        if pd.isna(prev_short) or pd.isna(prev_long) or pd.isna(curr_short) or pd.isna(curr_long):
            signals.append(0)
            continue

        # Golden cross (buy signal)
        if prev_short <= prev_long and curr_short > curr_long:
            signals.append(1)
        # Death cross (sell signal)
        elif prev_short >= prev_long and curr_short < curr_long:
            signals.append(-1)
        else:
            signals.append(0)

    # Prepend 0 for first row
    return [0] + signals
