import requests

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"
SYMBOL = "BTCUSDT"

def get_current_price():
    try:
        response = requests.get(BINANCE_API_URL, params={"symbol": SYMBOL})
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except (requests.RequestException, ValueError, KeyError):
        
        return None