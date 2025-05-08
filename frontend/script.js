const BACKEND_URL = "http://127.0.0.1:8000";


async function fetchPrice() {
    try {
        const response = await fetch(`${BACKEND_URL}/price`);
        const data = await response.json();
        document.getElementById('price').innerText = `Cena: ${data.price} USD`;
    } catch (error) {
        console.error('Błąd pobierania ceny:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchPrice();
});

async function fetchTodayRSI() {
    try {
        const response = await fetch(`${BACKEND_URL}/analyze/rsi/today`);
        const data = await response.json();
        document.getElementById('rsi-value').innerText = `${data.today_rsi}`;
    } catch (error) {
        console.error('Błąd pobierania RSI:', error);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    fetchTodayRSI();
});

async function fetchMarketCap() {
    try {
        const response = await fetch(`${BACKEND_URL}/market_cap`);
        const data = await response.json();
        document.getElementById('market-cap-value').innerText = `${data.market_cap} USD`;
    } catch (error) {
        console.error('Błąd pobierania kapitalizacji rynkowej:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchMarketCap();
});


async function fetchDominance() {
    try {
        const response = await fetch(`${BACKEND_URL}/dominance`);
        const data = await response.json();
        document.getElementById('domiance-value').innerText = `${data.dominance} %`;
    } catch (error) {
        console.error('Błąd pobierania kapitalizacji rynkowej:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchDominance();
})

async function fetchRedditTitles() {
    try {
        const response = await fetch(`${BACKEND_URL}/reddit`);
        const data = await response.json();
        displayTitles(data.titles);
    } catch (error) {
        console.error('Błąd:', error);
    }
}

function displayTitles(titles) {
    const titlesList = document.getElementById('news-item');
    titlesList.innerHTML = "";

    titles.forEach(title => {
        const li = document.createElement('li');
        li.textContent = title;
        titlesList.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', fetchRedditTitles);






const PERIOD_MAP = {
    "1D": { interval: "1h", limit: 24 },
    "7D": { interval: "1h", limit: 168 },
    "1M": { interval: "1d", limit: 30 },
    "3M": { interval: "1d", limit: 90 },
    "1Y": { interval: "1w", limit: 52 }
};

document.querySelector('.time-buttons').addEventListener('click', (event) => {
    if (event.target.classList.contains('time-btn')) {
        const period = event.target.getAttribute('data-period');
        const { interval, limit } = PERIOD_MAP[period] || { interval: "1d", limit: 30 };

        console.log(`Pobieram dane: interval=${interval}, limit=${limit}`);
        updateChart(interval, limit, true);  // Wymuszamy odświeżenie
    }
});

async function fetchHistoricalData(interval = "1d", limit = 30, force_refresh = false) {
    try {
        const response = await fetch(`${BACKEND_URL}/history?interval=${interval}&limit=${limit}&force_refresh=${force_refresh}`);
        const data = await response.json();
        console.log("Dane historyczne:", data);
        return data.data;
    } catch (error) {
        console.error('Błąd:', error);
        return null;
    }
}

async function updateChart(interval, limit, force_refresh = false) {
    const historicalData = await fetchHistoricalData(interval, limit, force_refresh);
    if (!historicalData) return;

    const labels = historicalData.map(item => new Date(item.open_time).getTime());
    const prices = historicalData.map(item => item.close);

    const ctx = document.getElementById('priceChart').getContext('2d');

    if (window.priceChart && window.priceChart instanceof Chart) {
        window.priceChart.destroy();
    }

    window.priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Cena BTCUSDT (${interval})`,
                data: prices,
                borderColor: 'rgb(255, 255, 255)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { type: 'time', time: { unit: 'day' } },
                y: { beginAtZero: false }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    updateChart('1d', 30, true);  // Wymuszamy odświeżenie na starcie
});
