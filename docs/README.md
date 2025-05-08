1. Charakterystyka oprogramowania

Bitcoin Sentiment App to aplikacja webowa, która analizuje sentyment rynku kryptowalutowego (BTC) z wykorzystaniem sztucznej inteligencji (OpenAI). Użytkownik może uzyskać aktualne dane rynkowe, analizować wskaźniki techniczne (np. RSI) oraz sprawdzić, jakie są nastroje inwestorów na podstawie postów z Reddita.
Celem aplikacji jest dostarczenie użytkownikowi szybkich i przystępnych informacji o rynku BTC bez podejmowania decyzji inwestycyjnych.

2. Specyfikacja wymagań
  2.1 Wymagania funkcjonalne i niefunkcjonalne
  ID	Nazwa	Opis wymagania	Typ	Priorytet
  F1	Pobieranie danych rynkowych	Aplikacja powinna automatycznie pobierać dane rynkowe z Binance i CoinGecko w czasie rzeczywistym.	Funkcjonalne	Wysoki
  F2	Wyświetlanie wskaźników	Użytkownik widzi aktualną cenę BTC, RSI oraz kapitalizację rynku.	Funkcjonalne	Wysoki
  F3	Analiza sentymentu	Użytkownik może wysłać dane rynkowe do OpenAI, aby uzyskać analizę sentymentu rynku BTC.	Funkcjonalne	Wysoki
  F4	Pobieranie tytułów z Reddita	Aplikacja powinna pobierać tytuły postów z Reddita i wyświetlać je w formie listy.	Funkcjonalne	Średni
  NF1	Intuicyjny interfejs	Interfejs użytkownika musi być prosty i przyjazny w obsłudze.	Niefunkcjonalne	Średni
  NF2	Aktualizacja danych	Dane rynkowe powinny być odświeżane w tle, bez przeładowania strony.	Niefunkcjonalne	Średni
  NF3	Responsywność	Aplikacja musi działać poprawnie na urządzeniach mobilnych.	Niefunkcjonalne	Średni

3. Architektura i stos technologiczny
  3.1 Architektura uruchomieniowa (run-time)
  Typ: Architektura klient-serwer
  [Frontend (HTML, CSS, JavaScript, Chart.js)] ⇄ [API (FastAPI, Python)] ⇄ [Dane rynkowe z Binance, CoinGecko, Reddit, OpenAI]

3.2 Architektura testowa
  Testy manualne działania interfejsu użytkownika.
  Testy poprawności struktury zwracanych danych (JSON).
  Testowanie obsługi cache (czas ważności, odświeżanie danych).
  Obsługa błędów (np. brak danych z API, nieprawidłowy klucz API OpenAI).

3.3 Stos technologiczny
  Warstwa	Technologia
  Frontend	HTML, CSS, JavaScript, Chart.js
  Backend	Python, FastAPI, Uvicorn
  Komunikacja	REST API, fetch(), JSON
  Inne	CORS, Cache, OpenAI, Binance, CoinGecko, BeautifulSoup

3.4 Procedura instalacji (lokalnie)
Backend:
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  uvicorn main:app --reload
  Dostępne pod http://127.0.0.1:8000.

Frontend:
  cd frontend
  python -m http.server
  Otwiera się w przeglądarce pod http://127.0.0.1:8000 lub na innym porcie wskazanym przez serwer.

3.5 Procedura rozwoju
  Wszelkie zmiany w kodzie frontendowym i backendowym muszą być wersjonowane w GitHubie.
  Każdy commit powinien zawierać opis w formacie:
  [MOD] Dodano obsługę cache dla przycisków
  [FIX] Poprawiono responsywność wykresu
  Po każdej większej aktualizacji należy przeprowadzić testy endpointów /price, /history, /predict.

4. Scenariusze testów
4.1 Test pobierania aktualnej ceny BTC
  Cel: Sprawdzić, czy aplikacja poprawnie pobiera i wyświetla aktualną cenę BTC.
  Wejście: Żądanie GET na endpoint /price.
  Oczekiwany wynik: Status 200 OK, zwrócony JSON z ceną BTC.

4.2 Test pobierania danych historycznych
  Cel: Sprawdzić, czy aplikacja zwraca poprawne dane historyczne.
  Wejście: Żądanie GET na endpoint /history?interval=1d&limit=7.
  Oczekiwany wynik: Status 200 OK, lista świec z open_time i close.

4.3 Test analizy sentymentu
  Cel: Sprawdzić, czy aplikacja poprawnie generuje analizę sentymentu na podstawie danych rynkowych i postów z Reddita.
  Wejście: Żądanie POST na endpoint /predict z kluczem API OpenAI.
  Oczekiwany wynik: Status 200 OK, zwrócony tekst analizy AI.

4.4 Test błędu przy braku klucza API
  Cel: Sprawdzić, czy aplikacja zwraca odpowiedni komunikat błędu, gdy klucz API OpenAI jest pusty.
  Wejście: Żądanie POST na /predict bez api_key.
  Oczekiwany wynik: Status 400 Bad Request, komunikat "Klucz API jest wymagany".

4.5 Test odświeżania cache dla przycisków
  Cel: Sprawdzić, czy kliknięcie przycisków zmienia force_refresh i odświeża dane wykresu.
  Wejście: Kliknięcie przycisku "1D", "7D", "1M".
  Oczekiwany wynik: Dane są odświeżone i różnią się od poprzednich (jeśli są nowe dane).

4.6 Test błędu przy niedostępności API Binance
  Cel: Sprawdzić, czy aplikacja obsługuje błąd, gdy API Binance zwraca 500 Internal Server Error.
  Wejście: Symulacja błędu 500 z Binance.
  Oczekiwany wynik: Status 500 Internal Server Error, komunikat "Błąd podczas pobierania danych z Binance".

5. Uwagi końcowe:
  Aplikacja nie oferuje możliwości inwestowania ani handlu kryptowalutami.
  Wszystkie dane są pobierane w czasie rzeczywistym i mogą się zmieniać dynamicznie.

6. Informacja prawna dotycząca projektu Bitcoin Sentiment App:
  Projekt Bitcoin Sentiment App został stworzony w celach edukacyjnych przez zespół projektowy w ramach zajęć akademickich. Informacje generowane przez aplikację mają charakter wyłącznie informacyjny i nie stanowią rekomendacji inwestycyjnych w rozumieniu Rozporządzenia   Ministra Finansów z dnia 19 października 2005 roku w sprawie informacji stanowiących rekomendacje dotyczące instrumentów finansowych, ich emiterów lub wystawców (Dz. U. z 2005 roku, Nr 206, poz. 1715).

  Aplikacja analizuje dane rynkowe i generuje analizy sentymentu przy użyciu modeli sztucznej inteligencji (OpenAI). Wyniki analiz nie powinny być traktowane jako porady inwestycyjne i nie mogą być podstawą do podejmowania decyzji finansowych. Autorzy projektu nie         ponoszą   odpowiedzialności za decyzje inwestycyjne podjęte na podstawie wyników generowanych przez aplikację. Każda decyzja inwestycyjna podejmowana jest na wyłączną odpowiedzialność użytkownika.

