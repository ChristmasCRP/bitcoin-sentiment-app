import requests

def get_bitcoin_market_cap() -> float:
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin")
        response.raise_for_status()
        coin_data = response.json()
        return coin_data["market_data"]["market_cap"]["usd"]
    except Exception as e:
        print(f"Błąd podczas pobierania market cap: {e}")
        return 0.0

def get_bitcoin_dominance() -> float:
    try:
        response = requests.get("https://api.coingecko.com/api/v3/global")
        response.raise_for_status()
        data = response.json()
        return data["data"]["market_cap_percentage"]["btc"]
    except Exception as e:
        print(f"Błąd podczas pobierania dominacji: {e}")
        return 0.0
