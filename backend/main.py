import requests
from fastapi import FastAPI, Query, HTTPException
from typing import List
from pydantic import BaseModel
from backend.services.binance_service import get_current_price, get_historical_data
from backend.services.scraping_service import get_reddit_titles_cached
from backend.processing.price_analyzer import calculate_rsi, calculate_today_rsi
from backend.services.openai_service import make_prediction
from backend.models.price_data import PredictionRequest
from backend.services.coingeco_service import get_bitcoin_market_cap, get_bitcoin_dominance

app = FastAPI()

from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/price")
def read_price():
    price = get_current_price()
    if price is None:
        raise HTTPException(status_code=500, detail="Nie udało się pobrać ceny z Binance")
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
    market_cap = get_bitcoin_market_cap()
    return {"market_cap": market_cap}

@app.get("/dominance")
def read_dominance():
    dominance = get_bitcoin_dominance()
    return {"dominance": dominance}

    
class PredictionRequest(BaseModel):
    api_key: str

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        price = get_current_price()

        rsi_data = get_historical_data(interval="1d", limit=15)
        rsi = calculate_today_rsi(rsi_data, period=14)

        market_cap = get_bitcoin_market_cap()
        dominance = get_bitcoin_dominance()

        reddit_titles = get_reddit_titles_cached(subreddit="Bitcoin", limit=5)

        history_data = get_historical_data(interval="1d", limit=7)
        history = [str(day["close"]) for day in history_data[-7:]]

        prediction = make_prediction(
            request.api_key,
            price,
            rsi,
            dominance,
            market_cap,
            reddit_titles,
            history
        )
        
        return {"prediction": prediction}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))