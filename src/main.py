import sys
from src.simulator import Simulator

def main():
    symbol = "AAPL"
    initial_cash = 100000
    commission_rate = 0.001

    if len(sys.argv) > 1:
        symbol = sys.argv[1]
    if len(sys.argv) > 2:
        initial_cash = int(sys.argv[2])
    if len(sys.argv) > 3:
        commission_rate = float(sys.argv[3])

    print(f"Running simulation for {symbol}")
    print(f"Initial cash: ${initial_cash:,.2f}")
    print(f"Commission rate: {commission_rate*100}%")
    print()

    simulator = Simulator(symbol, initial_cash, commission_rate)
    success = simulator.run(use_demo=True)

    if success:
        results = simulator.get_results()
        print(f"Simulation Results:")
        print(f"  Final Equity: ${results['final_equity']:,.2f}")
        print(f"  Total Return: {results['total_return']}%")
        print(f"  Sharpe Ratio: {results['sharpe_ratio']}")
        print(f"  Max Drawdown: {results['max_drawdown']}%")
        print(f"  Win Rate: {results['win_rate']}%")
        print(f"  Total Trades: {results['total_trades']}")
    else:
        print("Simulation failed")

if __name__ == "__main__":
    main()
