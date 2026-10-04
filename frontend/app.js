let chart = null;

document.getElementById('simulate-btn').addEventListener('click', runSimulation);

async function runSimulation() {
    const symbol = document.getElementById('symbol').value.toUpperCase();
    const initial_cash = parseInt(document.getElementById('initial_cash').value);
    const commission_rate = parseFloat(document.getElementById('commission_rate').value) / 100;

    if (!symbol || initial_cash <= 0) {
        showError('Please enter valid values');
        return;
    }

    showLoading(true);
    hideError();
    hideResults();

    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symbol: symbol,
                initial_cash: initial_cash,
                commission_rate: commission_rate,
                use_demo: true
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Simulation failed');
        }

        const results = await response.json();
        displayResults(results);
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

function displayResults(results) {
    document.getElementById('final_equity').textContent = `$${results.final_equity.toLocaleString()}`;
    document.getElementById('total_return').textContent = `${results.total_return}%`;
    document.getElementById('sharpe_ratio').textContent = results.sharpe_ratio;
    document.getElementById('max_drawdown').textContent = `${results.max_drawdown}%`;
    document.getElementById('win_rate').textContent = `${results.win_rate}%`;
    document.getElementById('total_trades').textContent = results.total_trades;

    displayTradeHistory(results.trade_records);
    displayEquityChart(results.equity_records);

    showResults();
}

function displayTradeHistory(trades) {
    const tbody = document.getElementById('trades-body');
    tbody.innerHTML = '';

    trades.forEach(trade => {
        const row = document.createElement('tr');
        row.classList.add(trade.action === 'BUY' ? 'buy' : 'sell');
        row.innerHTML = `
            <td>${new Date(trade.date).toLocaleDateString()}</td>
            <td>${trade.action}</td>
            <td>${trade.shares}</td>
            <td>$${trade.price.toFixed(2)}</td>
            <td>$${trade.commission.toFixed(2)}</td>
            <td>$${trade.total.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
    });
}

function displayEquityChart(equityRecords) {
    const ctx = document.getElementById('equity-chart').getContext('2d');

    const dates = equityRecords.map(e => new Date(e.date).toLocaleDateString());
    const equities = equityRecords.map(e => e.equity);

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Portfolio Equity',
                data: equities,
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 2,
                pointBackgroundColor: '#2196F3',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#333',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function showResults() {
    document.getElementById('results').style.display = 'block';
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showError(message) {
    document.getElementById('error').style.display = 'block';
    document.getElementById('error-message').textContent = message;
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        if (!response.ok) {
            showError('Failed to connect to API');
        }
    } catch (error) {
        showError('Failed to connect to API: ' + error.message);
    }
});
