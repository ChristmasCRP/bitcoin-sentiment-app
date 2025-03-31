import pandas as pd
from typing import List, Dict
import numpy as np

def calculate_rsi(data: List[Dict], period: int = 14) -> List[float]:
    """
    Oblicza wskaźnik RSI na podstawie danych historycznych.
    """
    # Pobieramy ceny zamknięcia z danych
    closes = [candle['close'] for candle in data]

    if len(closes) < period + 1:
        raise ValueError("Za mało danych do obliczenia RSI")

    # Tworzymy pandas Series
    series = pd.Series(closes)
    
    # Liczymy różnicę pomiędzy kolejnymi dniami
    delta = series.diff().dropna()
    
    # Obliczamy zyski i straty
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # Obliczamy średnie za pomocą rolling().mean()
    avg_gain = pd.Series(gain).rolling(window=period, min_periods=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period, min_periods=period).mean()

    # Wypełniamy wartości NaN, żeby uniknąć błędów
    avg_gain.fillna(0, inplace=True)
    avg_loss.fillna(0, inplace=True)

    # Obliczamy RS i RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Zamieniamy wartości 0 i 100 na None, żeby ich nie zwracać w odpowiedzi
    rsi = rsi.replace([np.inf, -np.inf], np.nan).fillna(method='bfill').tolist()

    # Wstawianie None na początkowych pozycjach
    rsi = [None] * (len(data) - len(rsi)) + rsi

    return rsi

def calculate_today_rsi(data: List[Dict], period: int = 14) -> float:
    """
    Oblicza RSI tylko dla najnowszej świeczki.
    """
    rsi_values = calculate_rsi(data, period)
    last_value = rsi_values[-1]
    return last_value if last_value is not None else None
