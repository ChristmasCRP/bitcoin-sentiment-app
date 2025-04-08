import requests
from datetime import datetime
from typing import List, Dict, Any
import time

# URL do pobierania aktualnej ceny BTC/USDT
BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

# URL do pobierania danych historycznych
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"

def get_current_price():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        print("Wysyłam zapytanie do Binance API (aktualna cena)...")
        response = requests.get(BINANCE_PRICE_URL, params={"symbol": SYMBOL}, headers=headers)
        
        print("Status Code:", response.status_code)
        print("URL:", response.url)
        
        response.raise_for_status()
        data = response.json()
        
        print("Odpowiedź z Binance:", data)
        
        return float(data["price"])
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Błąd podczas pobierania ceny: {e}")
        return None
    

_cache_today_data = None
_cache_today_time = 0
_cache_duration = 600

def get_historical_data(interval: str = "1d", limit: int = 30, force_refresh: bool = False) -> List[Dict[str, Any]]:
    global _cache_today_data, _cache_today_time

    now = time.time()
    extra_data = 14

    if _cache_today_data is not None and not force_refresh and (now - _cache_today_time < _cache_duration):
        print("Dane zwrócone z cache")
        return _cache_today_data

    try:
        params = {
            "symbol": SYMBOL,
            "interval": interval,
            "limit": limit + extra_data
        }
        
        response = requests.get(BINANCE_KLINES_URL, params=params)
        response.raise_for_status()
        raw_data = response.json()
        
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
        
        _cache_today_data = historical_data
        _cache_today_time = now

        return historical_data

    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Błąd podczas pobierania danych historycznych: {e}")
        return []