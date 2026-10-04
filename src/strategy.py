class MAStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df):
        if df is None or len(df) == 0:
            return df

        if 'sma20' not in df.columns or 'sma50' not in df.columns:
            return df

        df['position'] = 0
        for i in range(1, len(df)):
            prev_sma20 = df.iloc[i-1].get('sma20')
            prev_sma50 = df.iloc[i-1].get('sma50')
            curr_sma20 = df.iloc[i].get('sma20')
            curr_sma50 = df.iloc[i].get('sma50')

            if prev_sma20 is not None and prev_sma50 is not None:
                if prev_sma20 <= prev_sma50 and curr_sma20 > curr_sma50:
                    df.at[df.index[i], 'position'] = 1
                elif prev_sma20 >= prev_sma50 and curr_sma20 < curr_sma50:
                    df.at[df.index[i], 'position'] = -1

        return df
