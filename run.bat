@echo off
cd /d "%~dp0"

python venv\Scripts\python.exe app.py
if errorlevel 1 (
    echo.
    echo Blad uruchamiania aplikacji.
    echo Sprawdz czy Python i biblioteki zostaly poprawnie zainstalowane.
    pause
)
