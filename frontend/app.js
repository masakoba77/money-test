// API Base URL
const API_BASE = window.location.origin === 'file://' ? 'http://localhost:8000' : window.location.origin;

// DOM Elements
const runBtn = document.getElementById('runBtn');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');

// Form inputs
const symbolsInput = document.getElementById('symbols');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const capitalInput = document.getElementById('capital');

// Chart instance
let equityChart = null;

// Event listeners
runBtn.addEventListener('click', runSimulation);

// Load default config on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE}/api/default-config`);
        const config = await response.json();

        symbolsInput.value = config.symbols.join(',');
        startDateInput.value = config.start_date;
        endDateInput.value = config.end_date;
        capitalInput.value = config.initial_capital;
    } catch (error) {
        console.error('Failed to load default config:', error);
    }
});

async function runSimulation() {
    try {
        // Clear previous errors
        hideError();

        // Get form values
        const symbols = symbolsInput.value
            .split(',')
            .map(s => s.trim().toUpperCase())
            .filter(s => s.length > 0);

        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const initialCapital = parseFloat(capitalInput.value);

        // Validation
        if (symbols.length === 0) {
            showError('銘柄を入力してください');
            return;
        }

        if (!startDate || !endDate) {
            showError('開始日と終了日を入力してください');
            return;
        }

        if (initialCapital <= 0) {
            showError('初期資金は0より大きい値を入力してください');
            return;
        }

        // Show loading
        showLoading();
        runBtn.disabled = true;

        // Call API
        const response = await fetch(`${API_BASE}/api/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symbols,
                start_date: startDate,
                end_date: endDate,
                initial_capital: initialCapital
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'シミュレーション失敗');
        }

        const data = await response.json();

        // Display results
        displayResults(data, initialCapital);

    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
        runBtn.disabled = false;
    }
}

function displayResults(data, initialCapital) {
    const stats = data.statistics;

    // Update statistics
    document.getElementById('statInitial').textContent = formatCurrency(initialCapital);
    document.getElementById('statFinal').textContent = formatCurrency(stats.final_value);

    const returnPct = stats.total_return_pct;
    const returnEl = document.getElementById('statReturn');
    returnEl.textContent = formatPercent(returnPct);
    returnEl.parentElement.classList.toggle('negative', returnPct < 0);
    returnEl.parentElement.classList.toggle('positive', returnPct > 0);

    document.getElementById('statTrades').textContent = stats.num_trades;

    const winRate = stats.num_trades > 0
        ? (stats.winning_trades / stats.num_trades * 100)
        : 0;
    document.getElementById('statWinRate').textContent = formatPercent(winRate, 1);

    const sharpeEl = document.getElementById('statSharpe');
    sharpeEl.textContent = stats.sharpe_ratio.toFixed(2);
    sharpeEl.parentElement.classList.toggle('positive', stats.sharpe_ratio > 0);
    sharpeEl.parentElement.classList.toggle('negative', stats.sharpe_ratio < 0);

    const drawdownEl = document.getElementById('statDrawdown');
    drawdownEl.textContent = formatPercent(stats.max_drawdown_pct, 2);
    drawdownEl.parentElement.classList.add('negative');

    // Draw chart
    drawEquityChart(data.equity_curve);

    // Fill trade table
    fillTradesTable(data.trades);

    // Show results
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function drawEquityChart(equityCurve) {
    const ctx = document.getElementById('equityChart').getContext('2d');

    const dates = equityCurve.map(d => formatDate(d.date));
    const values = equityCurve.map(d => d.equity);

    // Destroy previous chart
    if (equityChart) {
        equityChart.destroy();
    }

    const initialValue = values[0];
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);

    equityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Portfolio Value',
                data: values,
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    callbacks: {
                        label: function(context) {
                            return formatCurrency(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    ticks: {
                        maxTicksLimit: 10,
                    }
                },
                y: {
                    display: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });
}

function fillTradesTable(trades) {
    const tbody = document.getElementById('tradesBody');
    tbody.innerHTML = '';

    if (trades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-light);">トレード記録なし</td></tr>';
        return;
    }

    trades.forEach(trade => {
        const row = document.createElement('tr');

        const actionClass = trade.action === 'BUY' ? 'buy' : 'sell';
        const profitValue = trade.profit || 0;
        const profitClass = profitValue >= 0 ? 'profit' : 'loss';

        row.innerHTML = `
            <td>${formatDate(trade.date)}</td>
            <td>${trade.symbol}</td>
            <td class="${actionClass}">${trade.action}</td>
            <td>${trade.shares}</td>
            <td>$${trade.price.toFixed(2)}</td>
            <td class="${profitClass}">${profitValue ? formatCurrency(profitValue) : '-'}</td>
        `;

        tbody.appendChild(row);
    });
}

function showLoading() {
    loadingDiv.classList.remove('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
    errorDiv.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    errorDiv.classList.add('hidden');
}

// Utility functions
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(value);
}

function formatPercent(value, decimals = 2) {
    return (value >= 0 ? '+' : '') + value.toFixed(decimals) + '%';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}
