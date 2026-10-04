class MAStrategy:
    """Moving Average Crossover Strategy"""

    def __init__(self, short_ma=20, long_ma=50):
        self.short_ma = short_ma
        self.long_ma = long_ma

    def generate_signals(self, indicator_data):
        """Generate buy/sell signals from indicator data
        Returns list of signals: 1 (buy), -1 (sell), 0 (hold)
        """
        signals = []

        for i in range(len(indicator_data)):
            if i == 0:
                signals.append(0)
                continue

            curr = indicator_data.iloc[i]
            prev = indicator_data.iloc[i-1]

            # Check for NaN values
            if any(pd.isna(v) for v in [curr['sma_short'], curr['sma_long'],
                                         prev['sma_short'], prev['sma_long']]):
                signals.append(0)
                continue

            # Golden cross (short MA crosses above long MA) - BUY
            if prev['sma_short'] <= prev['sma_long'] and curr['sma_short'] > curr['sma_long']:
                signals.append(1)
            # Death cross (short MA crosses below long MA) - SELL
            elif prev['sma_short'] >= prev['sma_long'] and curr['sma_short'] < curr['sma_long']:
                signals.append(-1)
            else:
                signals.append(0)

        return signals

