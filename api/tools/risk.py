# api/tools/risk.py

import yfinance as yf
import numpy as np


def get_risk_metrics(ticker: str) -> dict:
    """
    Computes professional-grade risk metrics.
    Never raises exceptions.
    """

    try:
        stock = yf.download(ticker, period="1y", progress=False)
        market = yf.download("^GSPC", period="1y", progress=False)

        if stock.empty or market.empty:
            raise ValueError("Missing data")

        stock_ret = stock["Close"].pct_change().dropna()
        market_ret = market["Close"].pct_change().dropna()

        # Align time series
        min_len = min(len(stock_ret), len(market_ret))
        stock_ret = stock_ret[-min_len:]
        market_ret = market_ret[-min_len:]

        # ---- Beta ----
        beta = np.cov(stock_ret, market_ret)[0][1] / np.var(market_ret)

        # ---- Volatility (annualized) ----
        volatility = np.std(stock_ret) * np.sqrt(252)

        # ---- Max Drawdown ----
        cumulative = (1 + stock_ret).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min()

        # ---- Unified risk score (0–1) ----
        risk_score = min(
            max(abs(beta) * volatility, 0),
            1
        )

        # ---- Risk label ----
        if risk_score < 0.3:
            level = "Low"
        elif risk_score < 0.6:
            level = "Medium"
        else:
            level = "High"

        return {
            "beta": round(beta, 2),
            "volatility": round(volatility * 100, 2),
            "max_drawdown": round(max_drawdown * 100, 2),
            "risk_score": round(risk_score, 2),
            "level": level
        }

    except Exception:
        # Absolute-safe fallback
        return {
            "beta": None,
            "volatility": None,
            "max_drawdown": None,
            "risk_score": 0.5,
            "level": "Medium"
        }
