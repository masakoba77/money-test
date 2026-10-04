# US Stock Auto Trading Simulator

A Python-based web application for backtesting automated stock trading strategies using moving average crossover signals.

## Project Overview

This project provides both CLI and web-based interfaces for simulating US stock trading using a 20-day/50-day moving average crossover strategy. It calculates realistic performance metrics including Sharpe ratio, maximum drawdown, and win rate.

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (Chart.js)
- **Data Processing**: pandas, numpy
- **Trading Logic**: Custom backtesting engine with portfolio management
- **Database**: SQLite (for stock price caching)

## Key Features

### Backtesting Engine
- Multi-symbol support (AAPL, MSFT, etc.)
- Realistic simulation with 0.1% commission
- Daily rebalancing based on technical signals
- Complete trade history tracking

### Technical Analysis
- Simple Moving Averages (20-day, 50-day)
- Golden Cross / Death Cross signals
- RSI calculation (for future strategies)

### Performance Analysis
- Total return calculation
- Sharpe ratio (risk-adjusted returns)
- Maximum drawdown
- Win rate and trade count

### User Interface
- Responsive web app (iPhone compatible)
- Real-time simulation parameter adjustment
- Interactive equity curve chart (Chart.js)
- Trade history table
- Performance statistics display

## Project Structure

```
├── src/
│   ├── api.py              # FastAPI application & endpoints
│   ├── simulator.py        # Backtesting engine
│   ├── portfolio.py        # Portfolio management & P&L
│   ├── indicator.py        # Technical indicators
│   ├── strategy.py         # Trading strategy logic
│   ├── data_fetcher.py     # Data retrieval & caching
│   └── main.py             # CLI interface
├── frontend/
│   ├── index.html          # Web UI
│   ├── app.js              # Client-side logic
│   └── style.css           # Responsive styling
├── data/                    # Stock price database
├── output/                  # Simulation results
├── requirements.txt        # Python dependencies
├── run_server.sh          # Server startup script
└── CLAUDE.md              # This file
```

## Setup & Installation

### Prerequisites
- Python 3.11+
- pip or conda

### Installation Steps

```bash
# Clone repository
git clone https://github.com/masakoba77/money-test.git
cd money-test

# Install dependencies
pip install -r requirements.txt

# Run server
./run_server.sh

# Access web app
# PC: http://localhost:8000
# Mobile: http://<your-ip>:8000
```

## Usage

### Web App Mode (Recommended)

1. Start the FastAPI server: `./run_server.sh`
2. Open browser to `http://localhost:8000`
3. Configure:
   - Stock symbols (comma-separated)
   - Start/end dates
   - Initial capital
4. Click "Run Simulation"
5. View results and trade history

### CLI Mode

```bash
cd src
python main.py
```

## API Endpoints

- `GET /` - Serve web frontend
- `GET /api/health` - Health check
- `GET /api/default-config` - Get default configuration
- `POST /api/simulate` - Run simulation
  - Request body: `{symbols, start_date, end_date, initial_capital}`
  - Response: `{status, statistics, equity_curve, trades}`

## Trading Strategy

### 20-Day / 50-Day Moving Average Crossover

**Buy Signal** (Golden Cross):
- Short-term MA (20-day) crosses above long-term MA (50-day)
- Entry: Equal position size allocation across symbols

**Sell Signal** (Death Cross):
- Short-term MA drops below long-term MA
- Exit: Close entire position

## Performance Metrics

- **Total Return %**: (Final Value - Initial Capital) / Initial Capital × 100
- **Sharpe Ratio**: (Mean Daily Return / Std Dev Daily Return) × √252
- **Max Drawdown %**: (Lowest Equity - Peak Equity) / Peak Equity × 100
- **Win Rate**: Winning Trades / Total Trades × 100

## Known Limitations

1. **Demo Data**: Currently uses simulated stock prices (not real market data)
2. **No Slippage**: Executes at exact close prices
3. **No Market Constraints**: Doesn't account for liquidity or halts
4. **Single Strategy**: Currently limited to MA crossover
5. **No Real Trading**: Backtesting only (not connected to actual brokers)

## Future Enhancements

- [ ] Real market data integration (Yahoo Finance API)
- [ ] Multiple strategy support (RSI, MACD, Bollinger Bands)
- [ ] Parameter optimization (grid search, genetic algorithms)
- [ ] Machine learning predictions
- [ ] Risk management (stop-loss, position sizing)
- [ ] Docker containerization
- [ ] Cloud deployment (Heroku, AWS)
- [ ] User authentication & saved simulations
- [ ] Walk-forward analysis
- [ ] Real broker integration (Alpaca API)

## Development Notes

### Adding New Strategies

1. Create new strategy class in `strategy.py`
2. Implement `generate_signals()` method
3. Update API to accept strategy parameter
4. Add UI controls for strategy selection

### Improving Backtesting

1. Enhance `simulator.py` for:
   - Position sizing algorithms
   - Stop-loss implementation
   - Market impact simulation
2. Update `portfolio.py` for:
   - Advanced P&L calculations
   - Risk metrics (Sortino ratio, Calmar ratio)
   - Attribution analysis

### Frontend Customization

- Modify `frontend/style.css` for branding
- Add new chart types in `frontend/app.js`
- Implement dark/light mode toggle

## Testing

```bash
# Run simulation via API
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "symbols": ["AAPL"],
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "initial_capital": 100000
  }'
```

## Troubleshooting

**Issue**: "Port 8000 already in use"
- Solution: Change port in `run_server.sh` or kill existing process

**Issue**: "No data loaded"
- Solution: Check date range, ensure markets were open during period

**Issue**: "Module not found" errors
- Solution: Run `pip install -r requirements.txt` again

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit
3. Push to remote: `git push origin feature/your-feature`
4. Create Pull Request
5. After review and approval, merge to main

## License

MIT License - See LICENSE file for details

## Author

Claude Haiku 4.5 (AI Assistant)

## Disclaimer

This is an educational backtesting tool. Past performance does not guarantee future results. Use at your own risk. Not for real trading without proper risk management and broker integration.

---

**Last Updated**: October 2026
**Version**: 2.0 (Web App Edition)
