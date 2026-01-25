@echo off
echo Starting StockBot AI...
echo.
echo IMPORTANT: Run this from the project root directory!
echo.
echo Starting backend server in new window...
start "StockBot Backend" cmd /k "uvicorn api.main:app --reload --port 8000"
timeout /t 3 /nobreak >nul
echo.
echo Starting frontend in new window...
start "StockBot Frontend" cmd /k "cd ui && python -m streamlit run app.py"
echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
pause
