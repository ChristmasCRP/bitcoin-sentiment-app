from fastapi import FastAPI
from backend.services.binance_service import get_current_price
from backend.services.scraping_service import get_reddit_titles_cached

app = FastAPI()

@app.get("/price")
def read_price():
    price = get_current_price()
    if price is None:
        return {"error": "Nie udało się pobrać ceny z Binance"}
    return {"symbol": "BTCUSDT", "price": price}

@app.get("/reddit")
def read_reddit_titles():
    titles = get_reddit_titles_cached()
    return {"subreddit": "Bitcoin", "titles": titles}
