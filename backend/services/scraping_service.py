import requests
from bs4 import BeautifulSoup
import time
import re

_cached_data = None
_cached_time = 0
_cache_duration = 600

# Słowa kluczowe do filtrowania
KEYWORDS = ["bitcoin", "btc", "cryptocurrency", "blockchain"]

def get_reddit_titles(subreddit="Bitcoin", limit=10):
    url = f"https://old.reddit.com/r/{subreddit}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        posts = soup.find_all("div", class_="thing")
        titles = []

        for post in posts:
            title = post.find("a", class_="title")
            if title:
                title_text = title.get_text(strip=True)
                
                # Sprawdzamy czy tytuł zawiera przynajmniej jedno z słów kluczowych
                if any(re.search(rf"\b{kw}\b", title_text, re.IGNORECASE) for kw in KEYWORDS):
                    titles.append(title_text)
                
                # Zatrzymujemy się, gdy mamy odpowiednią ilość pasujących postów
                if len(titles) >= limit:
                    break

        return titles

    except Exception as e:
        return [f"Błąd podczas scrapowania Reddita: {e}"]

def get_reddit_titles_cached(subreddit="Bitcoin", limit=10):
    global _cached_data, _cached_time

    now = time.time()
    if _cached_data is not None and (now - _cached_time < _cache_duration):
        print("Zwrócone dane z cache")
        return _cached_data

    print("Nowe dane z reddita")
    data = get_reddit_titles(subreddit, limit)
    _cached_data = data
    _cached_time = now
    return data