import pandas as pd
from src.portfolio import Portfolio
from src.indicator import add_indicators, assign_signals
from src.strategy import MAStrategy
from src.data_fetcher import fetch_data, generate_demo_data

class Simulator:
    def __init__(self, symbol, initial_cash=100000, commission_rate=0.001):
        self.symbol = symbol
        self.initial_cash = initial_cash
        self.commission_rate = commission_rate
        self.portfolio = None
        self.data = None
        self.results = None

    def run(self, start_date=None, end_date=None, use_demo=True):
        if use_demo:
            self.data = generate_demo_data(days=250, symbol=self.symbol)
        else:
            self.data = fetch_data(self.symbol, start_date, end_date)

        if self.data is None or len(self.data) == 0:
            return False

        self.data = add_indicators(self.data)
        self.data = assign_signals(self.data)

        self.portfolio = Portfolio(self.initial_cash, self.commission_rate)

        for idx, row in self.data.iterrows():
            date = row['date']
            close_price = row['close']
            signal = row.get('signal', 'HOLD')

            current_prices = {self.symbol: close_price}

            if signal == 'GOLDEN_CROSS':
                if self.symbol not in self.portfolio.positions:
                    shares_to_buy = int(self.portfolio.cash / (close_price * 1.001) * 0.95)
                    if shares_to_buy > 0:
                        self.portfolio.buy(date, self.symbol, shares_to_buy, close_price)

            elif signal == 'DEATH_CROSS':
                if self.symbol in self.portfolio.positions:
                    shares_to_sell = self.portfolio.positions[self.symbol]['shares']
                    self.portfolio.sell(date, self.symbol, shares_to_sell, close_price)

            self.portfolio.snapshot_equity(date, current_prices)

        return True

    def get_results(self):
        if self.portfolio is None:
            return None

        equity_records = []
        for snap in self.portfolio.equity_snapshots:
            equity_records.append({
                'date': snap['date'].isoformat() if hasattr(snap['date'], 'isoformat') else str(snap['date']),
                'equity': round(snap['equity'], 2),
                'cash': round(snap['cash'], 2)
            })

        trade_records = []
        for trade in self.portfolio.trade_history:
            trade_records.append({
                'date': trade['date'].isoformat() if hasattr(trade['date'], 'isoformat') else str(trade['date']),
                'symbol': trade['symbol'],
                'action': trade['action'],
                'shares': trade['shares'],
                'price': round(trade['price'], 2),
                'commission': round(trade['commission'], 2),
                'total': round(trade['total'], 2)
            })

        stats = self.portfolio.calculate_performance_stats()

        self.results = {
            'symbol': self.symbol,
            'initial_cash': self.initial_cash,
            'final_equity': round(self.portfolio.get_total_value({self.symbol: self.data.iloc[-1]['close']}), 2),
            'total_return': round(stats['total_return'] * 100, 2),
            'sharpe_ratio': round(stats['sharpe_ratio'], 2),
            'max_drawdown': round(stats['max_drawdown'] * 100, 2),
            'win_rate': round(stats['win_rate'] * 100, 2),
            'total_trades': stats['total_trades'],
            'equity_records': equity_records,
            'trade_records': trade_records
        }

        return self.results
