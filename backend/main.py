from fastapi import FastAPI, Query
from backend.services.binance_service import get_current_price
from backend.services.scraping_service import get_reddit_titles_cached
from typing import List
from backend.services.binance_service import get_historical_data
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


@app.get("/analyze/rsi")
def read_rsi(
    interval: str = Query("1d", description="Przedział czasowy świeczek (np. '1d', '1h', '30m')"),
    limit: int = Query(15, description="Liczba świeczek do pobrania (np. 30)"),
    period: int = Query(14, description="Okres do obliczenia RSI (np. 14)"),
    force_refresh: bool = Query(False, description="Czy wymusić odświeżenie danych z Binance API")
):
    rsi_limit = limit + period

    data = get_historical_data(interval=interval, limit=rsi_limit, force_refresh=force_refresh)
    if not data:
        return {"error": "Nie udało się pobrać danych historycznych."}

    rsi_values = calculate_rsi(data, period)
    return {"symbol": "BTCUSDT", "interval": interval, "rsi": rsi_values}

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