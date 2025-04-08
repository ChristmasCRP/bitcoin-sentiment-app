from openai import OpenAI
from typing import List

def make_prediction(api_key: str, price: float, rsi: float, dominance: float, market_cap: float, reddit_titles: List[str], history: List[str]) -> str:
    try:
        print("Tworzę klienta OpenAI...")
        client = OpenAI(api_key=api_key)
        print("🔑 Używany klucz:", api_key[:15], "...")


        print("Generuję prompt...")
        prompt = f"""
        Jesteś analitykiem finansowym specjalizującym się w rynku kryptowalut.

        Oceń obecny sentyment na rynku na podstawie poniższych danych i określ, czy jest on pozytywny, negatywny czy neutralny. Nie udzielaj porady inwestycyjnej. 

        Dane:
        - Obecna cena Bitcoina: {price} USD.
        - RSI: {rsi}.
        - Dominacja: {dominance}%.
        - Kapitalizacja rynku: {market_cap} USD.
        - Ostatnie tytuły z Reddita: {', '.join(reddit_titles)}.
        - Historia cen Bitcoina (7 dni): {', '.join(history)}.

        Napisz jedno krótkie zdanie podsumowujące sentyment rynkowy, bez użycia słów 'kupuj' ani 'sprzedaj'. Nie udzielaj porady inwestycyjnej.
        """

        print("Wysyłam zapytanie do OpenAI...")
       
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst specialized in cryptocurrency."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )

        print("Odpowiedź z OpenAI otrzymana...")
        prediction = response.choices[0].message.content.strip()
        print("Treść odpowiedzi modelu:", response.choices[0].message.content)

        if not prediction:
            prediction = "Nie udało się określić sentymentu."


        return prediction

    except Exception as e:
        raise Exception(f"Błąd podczas przetwarzania zapytania: {str(e)}")  