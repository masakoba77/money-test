from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from src.simulator import Simulator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    symbol: str = "AAPL"
    initial_cash: int = 100000
    commission_rate: float = 0.001
    use_demo: bool = True

class SimulationResponse(BaseModel):
    symbol: str
    initial_cash: int
    final_equity: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    equity_records: list
    trade_records: list

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Stock Simulator API is running"}

@app.get("/api/default-config")
def default_config():
    return {
        "symbol": "AAPL",
        "initial_cash": 100000,
        "commission_rate": 0.001,
        "sma_short": 20,
        "sma_long": 50
    }

@app.post("/api/simulate")
def simulate(request: SimulationRequest):
    try:
        simulator = Simulator(
            symbol=request.symbol,
            initial_cash=request.initial_cash,
            commission_rate=request.commission_rate
        )

        success = simulator.run(use_demo=request.use_demo)
        if not success:
            raise HTTPException(status_code=500, detail="Simulation failed")

        results = simulator.get_results()
        return SimulationResponse(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
