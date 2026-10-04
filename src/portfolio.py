import pandas as pd
import numpy as np
from datetime import datetime

class Portfolio:
    def __init__(self, initial_cash=100000, commission_rate=0.001):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.commission_rate = commission_rate
        self.positions = {}
        self.equity_snapshots = []
        self.trade_history = []
        self.peak_equity = initial_cash

    def buy(self, date, symbol, shares, price):
        if shares <= 0 or price <= 0:
            return False

        cost = shares * price * (1 + self.commission_rate)
        if cost > self.cash:
            return False

        self.cash -= cost
        if symbol not in self.positions:
            self.positions[symbol] = {'shares': 0, 'avg_price': 0}

        pos = self.positions[symbol]
        total_value = pos['shares'] * pos['avg_price'] + shares * price
        pos['shares'] += shares
        pos['avg_price'] = total_value / pos['shares'] if pos['shares'] > 0 else price

        commission = shares * price * self.commission_rate
        self.trade_history.append({
            'date': date,
            'symbol': symbol,
            'action': 'BUY',
            'shares': shares,
            'price': price,
            'commission': commission,
            'total': cost
        })
        return True

    def sell(self, date, symbol, shares, price):
        if symbol not in self.positions or shares <= 0 or price <= 0:
            return False

        if self.positions[symbol]['shares'] < shares:
            return False

        proceeds = shares * price * (1 - self.commission_rate)
        self.cash += proceeds
        self.positions[symbol]['shares'] -= shares

        if self.positions[symbol]['shares'] == 0:
            del self.positions[symbol]

        commission = shares * price * self.commission_rate
        self.trade_history.append({
            'date': date,
            'symbol': symbol,
            'action': 'SELL',
            'shares': shares,
            'price': price,
            'commission': commission,
            'total': proceeds
        })
        return True

    def get_position_value(self, symbol, current_price):
        if symbol not in self.positions:
            return 0
        return self.positions[symbol]['shares'] * current_price

    def get_total_value(self, current_prices):
        total = self.cash
        for symbol, pos in self.positions.items():
            if symbol in current_prices:
                total += pos['shares'] * current_prices[symbol]
        return total

    def snapshot_equity(self, date, current_prices):
        total_value = self.get_total_value(current_prices)
        self.equity_snapshots.append({
            'date': date,
            'equity': total_value,
            'cash': self.cash,
            'positions': dict(self.positions)
        })
        if total_value > self.peak_equity:
            self.peak_equity = total_value
        return total_value

    def calculate_performance_stats(self):
        if len(self.equity_snapshots) < 2:
            return {
                'total_return': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'win_rate': 0,
                'total_trades': 0
            }

        equity_values = [snap['equity'] for snap in self.equity_snapshots]
        dates = [snap['date'] for snap in self.equity_snapshots]

        total_return = (equity_values[-1] - self.initial_cash) / self.initial_cash

        daily_returns = pd.Series(equity_values).pct_change().dropna()
        if len(daily_returns) > 0 and daily_returns.std() > 0:
            sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0

        cumulative_max = pd.Series(equity_values).cummax()
        drawdown = (pd.Series(equity_values) - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min()

        winning_trades = sum(1 for t in self.trade_history if t['action'] == 'SELL' and t['total'] > 0)
        total_trades = len([t for t in self.trade_history if t['action'] == 'BUY'])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': total_trades
        }
