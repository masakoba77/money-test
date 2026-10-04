import pandas as pd
from portfolio import Portfolio
from indicator import add_indicators
from strategy import MAStrategy

class Simulator:
    """Backtesting simulator for stock trading strategies"""

    def __init__(self, initial_capital=100000, commission=0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.portfolio = Portfolio(initial_capital, commission)
        self.strategy = MAStrategy()

    def run(self, stocks_data):
        """Run simulation on stock data
        stocks_data: dict of {symbol: dataframe with OHLCV}
        """
        # Merge all stock data by date
        all_data = {}
        for symbol, df in stocks_data.items():
            all_data[symbol] = add_indicators(df.copy())

        # Get all unique dates sorted
        all_dates = set()
        for symbol, df in all_data.items():
            all_dates.update(df.index)

        all_dates = sorted(list(all_dates))

        # Simulate day by day
        for date in all_dates:
            current_prices = {}
            signals = {}

            # Collect current prices and signals for all symbols
            for symbol, df in all_data.items():
                if date in df.index:
                    current_prices[symbol] = df.loc[date, 'close']

                    # Generate signals from indicator
                    idx = df.index.get_loc(date)

                    if idx > 0:
                        prev_row = df.iloc[idx-1]
                        curr_row = df.iloc[idx]

                        # Check if we have valid indicator values
                        if not pd.isna(curr_row['sma_short']) and not pd.isna(curr_row['sma_long']) and \
                           not pd.isna(prev_row['sma_short']) and not pd.isna(prev_row['sma_long']):

                            # Golden cross: buy
                            if prev_row['sma_short'] <= prev_row['sma_long'] and \
                               curr_row['sma_short'] > curr_row['sma_long']:
                                signals[symbol] = 1
                            # Death cross: sell
                            elif prev_row['sma_short'] >= prev_row['sma_long'] and \
                                 curr_row['sma_short'] < curr_row['sma_long']:
                                signals[symbol] = -1
                            else:
                                signals[symbol] = 0
                        else:
                            signals[symbol] = 0
                    else:
                        signals[symbol] = 0

            # Execute trades based on signals
            for symbol, signal in signals.items():
                if symbol not in current_prices:
                    continue

                current_price = current_prices[symbol]
                position = self.portfolio.positions.get(symbol, {})

                if signal == 1:  # Buy signal
                    # Only buy if we don't already hold this stock
                    if position.get('shares', 0) == 0:
                        # Allocate equal amount to each symbol
                        shares_to_buy = int((self.portfolio.cash / len(all_data)) / current_price)
                        if shares_to_buy > 0:
                            self.portfolio.buy(symbol, shares_to_buy, current_price, date)

                elif signal == -1:  # Sell signal
                    # Sell all holdings of this stock
                    if position.get('shares', 0) > 0:
                        self.portfolio.sell(symbol, position['shares'], current_price, date)

            # Record daily equity value
            total_value = self.portfolio.get_total_value(current_prices)
            self.portfolio.record_equity(date, total_value)

        return self.portfolio

    def get_results(self):
        """Get simulation results"""
        stats = self.portfolio.get_performance_stats()

        return {
            'statistics': stats,
            'equity_curve': pd.DataFrame(self.portfolio.equity_history),
            'trades': pd.DataFrame(self.portfolio.trade_history),
            'portfolio': self.portfolio
        }
