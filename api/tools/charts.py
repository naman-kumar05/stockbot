# api/tools/charts.py

import yfinance as yf
import pandas as pd
import numpy as np


def get_price_chart(ticker: str, period: str = "6mo") -> dict:
    """
    Returns price + technical indicators for chart rendering.
    Safe, validated, never crashes.
    """

    try:
        df = yf.download(ticker, period=period, progress=False)

        if df.empty or len(df) < 20:
            return {"available": False}

        # ------------------------
        # Indicators
        # ------------------------

        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()

        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # ------------------------
        # Support / Resistance
        # ------------------------

        support = round(df["Low"].rolling(20).min().iloc[-1], 2)
        resistance = round(df["High"].rolling(20).max().iloc[-1], 2)

        # ------------------------
        # Trend
        # ------------------------

        trend = (
            "Uptrend"
            if df["MA20"].iloc[-1] > df["MA50"].iloc[-1]
            else "Downtrend"
        )

        # ------------------------
        # Chart data
        # ------------------------

        chart = []
        for idx, row in df.iterrows():
            chart.append({
                "date": idx.strftime("%Y-%m-%d"),
                "close": round(row["Close"], 2),
                "ma20": round(row["MA20"], 2) if not np.isnan(row["MA20"]) else None,
                "ma50": round(row["MA50"], 2) if not np.isnan(row["MA50"]) else None,
                "rsi": round(row["RSI"], 2) if not np.isnan(row["RSI"]) else None
            })

        return {
            "available": True,
            "trend": trend,
            "support": support,
            "resistance": resistance,
            "chart": chart[-120:]  # last ~6 months
        }

    except Exception:
        return {"available": False}
