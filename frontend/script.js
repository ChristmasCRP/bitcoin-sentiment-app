async function fetchPrice() {
    try {
        const response = await fetch('https://blablabla.blablabla/price');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('price').innerText = `Cena: ${data.price}`;
    } catch (error) {
        console.error('Błąd pobierania ceny:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchPrice();
});

async function fetchHistoricalData(period) {
    try {
        const response = await fetch(`https://blablabla.blablabla/history?period=${period}`);
        if (!response.ok) {
            throw new Error('Nie udało się pobrać danych.');
        }
        const data = await response.json();
        return data.data;
    } catch (error) {
        console.error('Błąd:', error);
        return null;
    }
}

async function updateChart(period) {
    const historicalData = await fetchHistoricalData(period);
    if (!historicalData) return;

    const labels = historicalData.map(item => item.timestamp);
    const prices = historicalData.map(item => item.price);

    if (window.priceChart) {
        window.priceChart.destroy();
    }

    const ctx = document.getElementById('priceChart').getContext('2d');
    window.priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Cena BTCUSDT (${period})`,
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

document.querySelector('.time-buttons').addEventListener('click', (event) => {
    if (event.target.classList.contains('time-btn')) {
        const period = event.target.getAttribute('data-period');
        updateChart(period);
    }
});

document.addEventListener('DOMContentLoaded', () => updateChart('1D'));

async function fetchRedditTitles() {
    try {
        const response = await fetch('https://blablabla.blablabla/reddit');
        if (!response.ok) {
            throw new Error('Błąd pobierania danych z Reddita');
        }
        const data = await response.json();
        displayTitles(data.titles);
    } catch (error) {
        console.error('Błąd:', error);
    }
}

function displayTitles(titles) {
    const titlesList = document.getElementById('reddit-titles');
    titlesList.innerHTML = "";

    titles.forEach(title => {
        const li = document.createElement('li');
        li.textContent = title;
        titlesList.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', fetchRedditTitles);

async function fetchTodayRSI() {
    try {
        const response = await fetch('https://blablabla.blablabla/analyze/rsi/today');
        if (!response.ok) {
            throw new Error('Błąd pobierania RSI.');
        }
        const data = await response.json();

        if (data.error) {
            document.getElementById('rsi-value').textContent = "Błąd pobierania danych.";
            return;
        }

        document.getElementById('rsi-value').textContent = `RSI: ${data.today_rsi}`;
    } catch (error) {
        console.error('Błąd:', error);
        document.getElementById('rsi-value').textContent = "Błąd ładowania RSI.";
    }
}

document.addEventListener('DOMContentLoaded', fetchTodayRSI);

async function fetchMarketCap() {
    try {
        const response = await fetch('https://blablabla.blablabla/market_cap');
        if (!response.ok) {
            throw new Error('Błąd pobierania Market Cap.');
        }
        const data = await response.json();

        if (!data.market_cap) {
            document.getElementById('market-cap-value').textContent = "Błąd ładowania danych.";
            return;
        }

        document.getElementById('market-cap-value').textContent = `Market Cap: ${data.market_cap.toLocaleString()} USD`;
    } catch (error) {
        console.error('Błąd:', error);
        document.getElementById('market-cap-value').textContent = "Błąd ładowania Market Cap.";
    }
}

document.addEventListener('DOMContentLoaded', fetchMarketCap);

async function fetchDominance() {
    try {
        const response = await fetch('https://blablabla.blablabla/dominance');
        if (!response.ok) {
            throw new Error('Błąd pobierania dominance.');
        }
        const data = await response.json();

        if (!data.dominance) {
            document.getElementById('dominance-value').textContent = "Błąd ładowania danych.";
            return;
        }

        document.getElementById('dominance-value').textContent = `Dominance: ${data.dominance.toFixed(2)}%`;
    } catch (error) {
        console.error('Błąd:', error);
        document.getElementById('dominance-value').textContent = "Błąd ładowania dominance.";
    }
}

document.addEventListener('DOMContentLoaded', fetchDominance);


