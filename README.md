# PDF Electrical Schematic Extractor

Aplikacja webowa do przetwarzania PDF z rysunkami schematów elektrycznych.

## Uruchomienie

1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

2. Upewnij się, że masz zainstalowany Tesseract OCR i Poppler.

3. Uruchom aplikację:
   ```bash
   python app.py
   ```

4. Otwórz w przeglądarce:
   ```text
   http://localhost:5000
   ```

## Funkcje

- wczytywanie PDF
- konwersja PDF do obrazów
- OCR tekstu z stron
- analiza urządzeń i połączeń
- eksport wyników do CSV, JSON i XLSX

## Uwagi

Projekt jest wersją startową i wymaga dalszego dopracowania logiki rozpoznawania połączeń i urządzeń na schematach elektrycznych.
