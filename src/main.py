import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from data_fetcher import fetch_and_save_stocks, load_from_database
from simulator import Simulator
import numpy as np

def generate_demo_data(symbol, start_date, end_date):
    """Generate demo stock data for testing"""
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # Filter out weekends (stock market closed)
    dates = dates[dates.weekday < 5]

    np.random.seed(hash(symbol) % 2**32)

    # Starting price
    start_price = {'AAPL': 145.0, 'MSFT': 320.0}.get(symbol, 100.0)

    # Generate random walk
    returns = np.random.normal(0.0003, 0.015, len(dates))
    prices = start_price * np.exp(np.cumsum(returns))

    data = {
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'High': prices * (1 + np.abs(np.random.normal(0, 0.01, len(dates)))),
        'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, len(dates)))),
        'Close': prices,
        'Volume': np.random.randint(10000000, 100000000, len(dates))
    }

    df = pd.DataFrame(data, index=dates)
    return df

def main():
    # Configuration
    symbols = ['AAPL', 'MSFT']
    start_date = '2023-01-01'
    end_date = '2024-09-30'
    initial_capital = 100000

    print("=" * 60)
    print("US Stock Auto Trading Simulator")
    print("=" * 60)
    print(f"Symbols: {', '.join(symbols)}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.0f}")
    print(f"Strategy: 20-day MA x 50-day MA Crossover")
    print("=" * 60)
    print()

    # Generate demo stock data
    print("Step 1: Generating demo stock data...")
    stocks_data = {}
    for symbol in symbols:
        data = generate_demo_data(symbol, start_date, end_date)
        stocks_data[symbol] = data
        print(f"  {symbol}: {len(data)} records")

    print("✓ Data generated\n")

    # Run simulation
    print("Step 2: Running simulation...")
    simulator = Simulator(initial_capital=initial_capital)
    portfolio = simulator.run(stocks_data)
    results = simulator.get_results()
    print("✓ Simulation complete\n")

    # Display results
    print("=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)

    stats = results['statistics']
    print(f"Initial Capital:     ${initial_capital:>12,.0f}")
    print(f"Final Value:         ${stats['final_value']:>12,.0f}")
    print(f"Total Return:        {stats['total_return_pct']:>12.2f}%")
    print(f"Total Trades:        {stats['num_trades']:>12}")
    print(f"Winning Trades:      {stats['winning_trades']:>12}")
    print(f"Win Rate:            {(stats['winning_trades']/max(stats['num_trades'],1)*100):>12.1f}%")
    print(f"Sharpe Ratio:        {stats['sharpe_ratio']:>12.2f}")
    print(f"Max Drawdown:        {stats['max_drawdown_pct']:>12.2f}%")
    print("=" * 60)
    print()

    # Save results to CSV
    print("Step 3: Saving results...")
    os.makedirs('output', exist_ok=True)

    results['equity_curve'].to_csv('output/equity_curve.csv', index=False)
    results['trades'].to_csv('output/trades.csv', index=False)
    print("✓ Results saved to output/")
    print()

    # Generate chart
    print("Step 4: Generating chart...")
    generate_chart(results)
    print("✓ Chart saved to output/backtest_chart.png")
    print()

    print("=" * 60)
    print("Simulation completed successfully!")
    print("=" * 60)

def generate_chart(results):
    """Generate backtest results chart"""
    equity_df = results['equity_curve'].copy()
    equity_df['date'] = pd.to_datetime(equity_df['date'])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Equity curve
    ax1.plot(equity_df['date'], equity_df['equity'], linewidth=2, color='blue')
    ax1.fill_between(equity_df['date'], equity_df['equity'], alpha=0.3, color='blue')
    ax1.set_title('Equity Curve', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    # Daily returns
    equity_df['daily_return'] = equity_df['equity'].pct_change() * 100
    colors = ['green' if x > 0 else 'red' for x in equity_df['daily_return'].fillna(0)]
    ax2.bar(equity_df['date'], equity_df['daily_return'], color=colors, alpha=0.6, width=1)
    ax2.set_title('Daily Returns', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Daily Return (%)', fontsize=12)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('output/backtest_chart.png', dpi=100, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()
