# ml/model/predict.py

import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# -----------------------------------
# Utilities
# -----------------------------------

def _safe_download(ticker: str, period: str):
    data = yf.download(ticker, period=period, progress=False)
    if data is None or data.empty:
        return None
    return data


def _confidence_from_error(mse: float, volatility: float) -> float:
    """
    Converts error + volatility into a bounded confidence score [0, 1]
    """
    score = 1 / (1 + mse * 10 + volatility * 5)
    return round(float(np.clip(score, 0.1, 0.95)), 2)


# -----------------------------------
# Short-Term Forecast
# -----------------------------------

def short_term_forecast(ticker: str) -> dict:
    """
    Forecasts next 5–10 trading days directionally.
    """

    data = _safe_download(ticker, "3mo")
    if data is None or len(data) < 30:
        return {
            "signal": "Neutral",
            "confidence": 0.3,
            "comment": "Insufficient recent data for short-term modeling."
        }

    close = data["Close"].values
    returns = np.diff(close) / close[:-1]

    X = np.arange(len(returns)).reshape(-1, 1)
    y = returns.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    preds = model.predict(X)
    mse = mean_squared_error(y, preds)

    volatility = np.std(returns) * np.sqrt(252)

    trend = model.coef_[0][0]

    if trend > 0.0005:
        signal = "Bullish"
    elif trend < -0.0005:
        signal = "Bearish"
    else:
        signal = "Neutral"

    confidence = _confidence_from_error(mse, volatility)

    return {
        "signal": signal,
        "confidence": confidence,
        "comment": "Short-term signal derived from recent momentum and volatility."
    }


# -----------------------------------
# Long-Term Forecast
# -----------------------------------

def long_term_forecast(ticker: str) -> dict:
    """
    Evaluates multi-year trend strength.
    """

    data = _safe_download(ticker, "5y")
    if data is None or len(data) < 200:
        return {
            "signal": "Neutral",
            "confidence": 0.4,
            "comment": "Insufficient long-term historical data."
        }

    prices = np.log(data["Close"].values)
    X = np.arange(len(prices)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, prices)

    trend = model.coef_[0]

    residuals = prices - model.predict(X)
    mse = np.mean(residuals ** 2)

    volatility = np.std(np.diff(prices))

    if trend > 0.0002:
        signal = "Bullish"
    elif trend < -0.0002:
        signal = "Bearish"
    else:
        signal = "Neutral"

    confidence = _confidence_from_error(mse, volatility)

    return {
        "signal": signal,
        "confidence": confidence,
        "comment": "Long-term outlook based on multi-year trend strength."
    }


# -----------------------------------
# Unified Interface (USED BY AGENT)
# -----------------------------------

def get_ml_outlook(ticker: str, horizon: str = "short_term") -> dict:
    """
    Main ML interface consumed by agent.
    """

    if horizon == "long_term":
        return long_term_forecast(ticker)

    return short_term_forecast(ticker)
