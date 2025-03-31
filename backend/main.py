from fastapi import FastAPI, Query
from backend.services.binance_service import get_current_price
from backend.services.scraping_service import get_reddit_titles_cached
from typing import List
from backend.services.binance_service import get_historical_data

app = FastAPI()

@app.get("/price")
def read_price():
    price = get_current_price()
    if price is None:
        return {"error": "Nie udało się pobrać ceny z Binance"}
    return {"symbol": "BTCUSDT", "price": price}

@app.get("/history")
def read_history(interval: str = Query("1d", description="Przedział czasowy świeczek (np. '1d', '1h', '30m')"),
                 limit: int = Query(30, description="Liczba świeczek do pobrania (np. 30)")):
    data = get_historical_data(interval=interval, limit=limit)
    if not data:
        return {"error": "Nie udało się pobrać danych historycznych."}
    return {"symbol": "BTCUSDT", "interval": interval, "data": data}

@app.get("/reddit")
def read_reddit_titles():
    titles = get_reddit_titles_cached()
    return {"subreddit": "Bitcoin", "titles": titles}
