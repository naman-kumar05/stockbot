from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

from ml.predict import predict_stock

app = FastAPI(title="StockBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    message: str


def extract_ticker(text: str):
    """
    Strategy:
    - Extract ALL uppercase words (1–5 chars)
    - Remove English words
    - RETURN THE LAST VALID CANDIDATE (AAPL comes after WHAT)
    """
    blacklist = {
        "WHAT", "SHOULD", "WITH", "ABOUT", "PRICE",
        "STOCK", "BUY", "SELL", "HOLD", "DO", "ME",
        "TELL", "TOP", "BEST"
    }

    candidates = re.findall(r"\b[A-Z]{1,5}\b", text.upper())

    valid = [c for c in candidates if c not in blacklist]

    if not valid:
        return None

    return valid[-1]   # 👈 KEY FIX


@app.get("/")
def root():
    return {"status": "StockBot API running"}


@app.post("/chat")
def chat(query: Query):
    ticker = extract_ticker(query.message)

    if not ticker:
        return {
            "error": "Please mention a valid stock ticker like AAPL, TSLA, MSFT"
        }

    try:
        result = predict_stock(ticker)
    except Exception as e:
        return {
            "error": f"Prediction failed for {ticker}",
            "details": str(e)
        }

    return {
        "ticker": result["ticker"],
        "current_price": result["current_price"],
        "predicted_price": result["predicted_price"],
        "expected_change_pct": result["expected_change_pct"],
        "signal": result["signal"],
        "explanation": (
            f"The model predicts a {result['expected_change_pct']}% move. "
            f"Signal: {result['signal']}."
        ),
    }
