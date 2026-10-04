# Stock Trading Simulator

A Python-based backtesting engine for US stock trading using a moving average crossover strategy with a responsive web UI.

## Features

- **Moving Average Crossover Strategy**: 20-day and 50-day simple moving average (SMA) crossover signals
- **Comprehensive Backtesting**: Full portfolio simulation with realistic trading costs
- **Performance Metrics**: Sharpe ratio, maximum drawdown, win rate, total return
- **Interactive Web UI**: Real-time results visualization with Chart.js
- **REST API**: FastAPI-based backend for easy integration
- **Docker Support**: Multi-stage Docker build for production deployment
- **CI/CD Pipeline**: GitHub Actions workflows for automated testing and deployment

## Quick Start

### Prerequisites
- Python 3.11+
- pip
- Optional: Docker and Docker Compose

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/masakoba77/money-test-java.git
cd money-test-java
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
bash run_server.sh
```

5. Open browser:
```
http://localhost:8000
```

### Docker Setup

1. Build the image:
```bash
docker build -t stock-simulator .
```

2. Run the container:
```bash
docker run -p 8000:8000 stock-simulator
```

Or use Docker Compose:
```bash
docker-compose up
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Default Configuration
```
GET /api/default-config
```

### Run Simulation
```
POST /api/simulate
Content-Type: application/json

{
  "symbol": "AAPL",
  "initial_cash": 100000,
  "commission_rate": 0.001,
  "use_demo": true
}
```

## Strategy Details

### Moving Average Crossover
- **Buy Signal (Golden Cross)**: When 20-day MA crosses above 50-day MA
- **Sell Signal (Death Cross)**: When 20-day MA crosses below 50-day MA
- **Position Sizing**: Uses 95% of available cash, reserved 5% as buffer
- **Commission**: 0.1% per trade (configurable)

### Performance Metrics
- **Total Return**: (Final Equity - Initial Cash) / Initial Cash
- **Sharpe Ratio**: Risk-adjusted return (annualized)
- **Max Drawdown**: Maximum peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Total Trades**: Number of buy signals

## Project Structure

```
money-test-java/
├── src/
│   ├── api.py              # FastAPI backend
│   ├── simulator.py        # Backtesting engine
│   ├── portfolio.py        # Portfolio management
│   ├── indicator.py        # Technical indicators
│   ├── strategy.py         # Trading strategy
│   ├── data_fetcher.py     # Data handling
│   └── main.py             # CLI entry point
├── frontend/
│   ├── index.html          # Web UI
│   ├── app.js              # Frontend logic
│   └── style.css           # Styling
├── .github/
│   ├── workflows/          # GitHub Actions workflows
│   └── ISSUE_TEMPLATE/     # Issue templates
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build
├── docker-compose.yml      # Docker Compose config
├── run_server.sh           # Server startup script
└── README.md               # This file
```

## Development

### Running Tests
```bash
pip install pytest pytest-cov
pytest src/tests/ -v --cov=src
```

### Code Quality
```bash
pip install flake8 pylint
flake8 src/
pylint src/
```

### Security Scanning
```bash
pip install bandit safety
bandit -r src/
safety check
```

## CI/CD

### Workflows
- **ci-cd.yml**: Build, test, and Docker image creation
- **pr-checks.yml**: Pull request validation
- **deploy.yml**: Release and deployment

See [CI-CD-SETUP.md](CI-CD-SETUP.md) for detailed configuration.

## Configuration

### GitHub Secrets (Optional)
- `DOCKER_REGISTRY_USERNAME`: Docker registry username
- `DOCKER_REGISTRY_PASSWORD`: Docker registry password

### Environment Variables
- `PYTHONUNBUFFERED=1`: For better Docker logging

## Documentation

- [CI/CD Setup Guide](CI-CD-SETUP.md)
- [GitHub Setup Guide](GITHUB-SETUP.md)

## License

MIT License

## Author

- Original Author: masakoba77
- Recreated in Python with FastAPI

## Support

For issues and feature requests, please use [GitHub Issues](https://github.com/masakoba77/money-test-java/issues).
