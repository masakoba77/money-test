import pandas as pd

class Portfolio:
    """Portfolio management for simulation"""

    def __init__(self, initial_capital=100000, commission=0.001):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.commission = commission  # 0.1% commission
        self.positions = {}  # {symbol: {shares: float, entry_price: float}}
        self.trade_history = []
        self.equity_history = []

    def buy(self, symbol, shares, price, date):
        """Buy shares of a stock"""
        cost = shares * price * (1 + self.commission)

        if cost > self.cash:
            # Not enough cash, buy what we can
            shares = int(self.cash / (price * (1 + self.commission)))
            if shares == 0:
                return 0
            cost = shares * price * (1 + self.commission)

        self.cash -= cost

        if symbol not in self.positions:
            self.positions[symbol] = {'shares': 0, 'entry_price': 0}

        # Update average entry price
        old_shares = self.positions[symbol]['shares']
        old_cost = old_shares * self.positions[symbol]['entry_price']
        new_cost = shares * price

        self.positions[symbol]['shares'] += shares
        self.positions[symbol]['entry_price'] = (old_cost + new_cost) / self.positions[symbol]['shares']

        self.trade_history.append({
            'date': date,
            'symbol': symbol,
            'action': 'BUY',
            'shares': shares,
            'price': price,
            'commission': cost - (shares * price)
        })

        return shares

    def sell(self, symbol, shares, price, date):
        """Sell shares of a stock"""
        if symbol not in self.positions or self.positions[symbol]['shares'] < shares:
            return 0

        proceeds = shares * price * (1 - self.commission)
        self.cash += proceeds

        profit = (price - self.positions[symbol]['entry_price']) * shares

        self.positions[symbol]['shares'] -= shares
        if self.positions[symbol]['shares'] == 0:
            del self.positions[symbol]

        self.trade_history.append({
            'date': date,
            'symbol': symbol,
            'action': 'SELL',
            'shares': shares,
            'price': price,
            'profit': profit,
            'commission': (shares * price) - proceeds
        })

        return shares

    def get_total_value(self, current_prices):
        """Get total portfolio value"""
        stock_value = 0
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                stock_value += position['shares'] * current_prices[symbol]

        return self.cash + stock_value

    def get_holdings(self):
        """Get current holdings"""
        return self.positions.copy()

    def record_equity(self, date, total_value):
        """Record daily equity value"""
        self.equity_history.append({
            'date': date,
            'equity': total_value
        })

    def get_performance_stats(self):
        """Calculate performance statistics"""
        if not self.equity_history:
            return {}

        df = pd.DataFrame(self.equity_history)
        df['date'] = pd.to_datetime(df['date'])

        final_value = df.iloc[-1]['equity']
        total_return = (final_value - self.initial_capital) / self.initial_capital * 100

        daily_returns = df['equity'].pct_change().dropna()

        sharpe_ratio = 0
        if daily_returns.std() != 0:
            sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * (252**0.5)

        max_equity = df['equity'].max()
        min_equity = df['equity'].min()
        max_drawdown = (min_equity - max_equity) / max_equity * 100 if max_equity != 0 else 0

        return {
            'total_return_pct': total_return,
            'final_value': final_value,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown_pct': max_drawdown,
            'num_trades': len(self.trade_history),
            'winning_trades': len([t for t in self.trade_history if t.get('profit', 0) > 0]),
        }
