@echo off
echo Starting StockBot Backend Server...
echo.
echo IMPORTANT: Run this from the project root directory!
echo.
uvicorn api.main:app --reload --port 8000
pause
