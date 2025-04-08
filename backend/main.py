import requests
from fastapi import FastAPI, Query
from typing import List
from backend.services.binance_service import get_current_price, get_historical_data
from backend.services.scraping_service import get_reddit_titles_cached
from backend.processing.price_analyzer import calculate_rsi, calculate_today_rsi

app = FastAPI()

@app.get("/price")
def read_price():
    price = get_current_price()
    if price is None:
        return {"error": "Nie udało się pobrać ceny z Binance"}
    return {"symbol": "BTCUSDT", "price": price}

@app.get("/history")
def read_history(
    interval: str = Query("1d", description="Przedział czasowy świeczek (np. '1d', '1h', '30m')"),
    limit: int = Query(30, description="Liczba świeczek do pobrania (np. 30)"),
    force_refresh: bool = Query(False, description="Czy wymusić odświeżenie danych z Binance API")
):
    data = get_historical_data(interval=interval, limit=limit, force_refresh=force_refresh)
    if not data:
        return {"error": "Nie udało się pobrać danych historycznych."}
    
    return {"symbol": "BTCUSDT", "interval": interval, "data": data}

@app.get("/reddit")
def read_reddit_titles():
    titles = get_reddit_titles_cached()
    return {"subreddit": "Bitcoin", "titles": titles}

@app.get("/analyze/rsi/today")
def analyze_today_rsi(
    interval: str = Query("1d"),
    period: int = Query(14)
):
    data = get_historical_data(interval=interval, limit=period + 1)
    if not data:
        return {"error": "Nie udało się pobrać danych historycznych."}
    today_rsi = calculate_today_rsi(data, period)
    return {"symbol": "BTCUSDT", "interval": interval, "today_rsi": today_rsi}

@app.get("/market_cap")
def read_market_cap():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin")
        response.raise_for_status()
        coin_data = response.json()
        
        market_cap = coin_data["market_data"]["market_cap"]["usd"]
        
        return {"market_cap": market_cap}
    except Exception as e:
        return {"error": f"Błąd podczas pobierania danych z CoinGecko: {str(e)}"}

@app.get("/dominance")
def read_dominance():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/global")
        response.raise_for_status()
        data = response.json()
        
        dominance = data["data"]["market_cap_percentage"]["btc"]
        
        return {"dominance": dominance}
    except Exception as e:
        return {"error": f"Błąd podczas pobierania danych z CoinGecko: {str(e)}"}
