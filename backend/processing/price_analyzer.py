import pandas as pd
from typing import List, Dict
import numpy as np

def calculate_rsi(data: List[Dict], period: int = 14) -> List[float]:
    closes = [candle['close'] for candle in data]

    if len(closes) < period + 1:
        raise ValueError("Za mało danych do obliczenia RSI")

    series = pd.Series(closes)
    delta = series.diff().dropna()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period, min_periods=1).mean()
    avg_loss = pd.Series(loss).rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    rsi = rsi.replace([np.inf, -np.inf], np.nan).tolist()
    rsi = [None if np.isnan(x) else x for x in rsi]

    rsi = [None] * (len(data) - len(rsi)) + rsi

    return rsi


def calculate_today_rsi(data: List[Dict], period: int = 14) -> float:
    rsi_values = calculate_rsi(data, period)
    return rsi_values[-1] if rsi_values else None
