from fastapi import FastAPI
from backend.services.binance_service import get_current_price

app = FastAPI()

@app.get("/price")
def read_price():
    price = get_current_price()
    if price is None:
        return {"error": "Nie udało się pobrać ceny"}
    return {"symbol": "BTCUSDT", "price": price}