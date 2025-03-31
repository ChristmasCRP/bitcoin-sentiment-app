import requests
from datetime import datetime
from typing import List, Dict, Any

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
    

BINANCE_API_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"

def get_historical_data(interval: str = "1d", limit: int = 30) -> List[Dict[str, Any]]:
    """
    Pobiera dane historyczne z Binance API.

    :param interval: Przedział czasowy świeczek (np. '1d', '1h', '30m')
    :param limit: Maksymalna liczba świeczek do pobrania (np. 30)
    :return: Lista słowników zawierających dane o świeczkach
    """
    try:
        params = {
            "symbol": SYMBOL,
            "interval": interval,
            "limit": limit
        }
        
        response = requests.get(BINANCE_API_URL, params=params)
        response.raise_for_status()
        raw_data = response.json()
        
        # Parsujemy dane do czytelnego formatu
        historical_data = []
        for candle in raw_data:
            historical_data.append({
                "open_time": datetime.utcfromtimestamp(candle[0] / 1000).isoformat() + "Z",
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
                "volume": float(candle[5]),
                "close_time": datetime.utcfromtimestamp(candle[6] / 1000).isoformat() + "Z"
            })
        
        return historical_data

    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Błąd podczas pobierania danych historycznych: {str(e)}")
        return []