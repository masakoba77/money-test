from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import json
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

from simulator import Simulator
from indicator import add_indicators
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

class SimulationRequest(BaseModel):
    symbols: list[str]
    start_date: str
    end_date: str
    initial_capital: float = 100000

class SimulationResponse(BaseModel):
    status: str
    statistics: dict
    equity_curve: list
    trades: list

def generate_demo_data(symbol, start_date, end_date):
    """Generate demo stock data"""
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = dates[dates.weekday < 5]

    np.random.seed(hash(symbol) % 2**32)
    start_price = {'AAPL': 145.0, 'MSFT': 320.0}.get(symbol, 100.0)

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

@app.get("/")
async def root():
    """Serve frontend"""
    return FileResponse("../frontend/index.html")

@app.get("/api/health")
async def health():
    """Health check"""
    return {"status": "ok"}

@app.post("/api/simulate")
async def simulate(request: SimulationRequest):
    """Run simulation"""
    try:
        # Validate input
        if not request.symbols or len(request.symbols) == 0:
            raise HTTPException(status_code=400, detail="No symbols provided")
        if request.initial_capital <= 0:
            raise HTTPException(status_code=400, detail="Initial capital must be positive")

        # Generate stock data
        stocks_data = {}
        for symbol in request.symbols:
            data = generate_demo_data(symbol, request.start_date, request.end_date)
            stocks_data[symbol] = data

        # Run simulation
        simulator = Simulator(initial_capital=request.initial_capital)
        portfolio = simulator.run(stocks_data)
        results = simulator.get_results()

        # Prepare response
        equity_df = results['equity_curve'].copy()
        equity_df['date'] = equity_df['date'].astype(str)

        trades_df = results['trades'].copy()
        trades_df['date'] = trades_df['date'].astype(str)

        return SimulationResponse(
            status="success",
            statistics=results['statistics'],
            equity_curve=equity_df.to_dict(orient='records'),
            trades=trades_df.to_dict(orient='records')
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/default-config")
async def default_config():
    """Get default simulation config"""
    return {
        "symbols": ["AAPL", "MSFT"],
        "start_date": "2023-01-01",
        "end_date": "2024-09-30",
        "initial_capital": 100000
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
