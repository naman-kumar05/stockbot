# api/tools/market.py

import yfinance as yf
import pandas as pd
import numpy as np


def _calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """Calculate RSI (Relative Strength Index)."""
    try:
        if len(prices) < period + 1:
            return None
        
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None
    except Exception:
        return None


def get_market_snapshot(ticker: str) -> dict:
    """
    Fetches latest market data for a ticker.
    Always returns a dict (never crashes).
    """

    try:
        stock = yf.Ticker(ticker)
        # Get more data for RSI calculation
        hist = stock.history(period="1mo", interval="1d")

        if hist.empty or len(hist) < 2:
            return {
                "price": None,
                "change": None,
                "change_pct": None,
                "trend": "Unknown",
                "rsi": None
            }

        latest_close = float(hist["Close"].iloc[-1])
        prev_close = float(hist["Close"].iloc[-2])

        change = latest_close - prev_close
        change_pct = (change / prev_close) * 100 if prev_close else 0.0

        # Trend logic
        if change_pct > 1:
            trend = "Uptrend"
        elif change_pct < -1:
            trend = "Downtrend"
        else:
            trend = "Sideways"
        
        # Calculate RSI
        rsi = _calculate_rsi(hist["Close"])

        return {
            "price": round(latest_close, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "trend": trend,
            "rsi": round(rsi, 2) if rsi is not None else None
        }

    except Exception:
        return {
            "price": None,
            "change": None,
            "change_pct": None,
            "trend": "Unavailable",
            "rsi": None
        }
