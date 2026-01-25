# api/tools/ml.py

from api.tools.market import get_market_snapshot


def ml_forecast(ticker: str) -> dict:
    """Wrapper for get_ml_outlook with default horizon."""
    return get_ml_outlook(ticker, horizon="short_term")


def get_ml_outlook(ticker: str, horizon: str = "short_term") -> dict:
    """
    ML + Technical hybrid logic.
    """

    market = get_market_snapshot(ticker)

    if not market:
        return {
            "signal": "Neutral",
            "confidence": 0.3,
            "comment": "Insufficient data for model inference."
        }

    rsi = market.get("rsi")
    trend = market.get("trend")

    signal = "Neutral"
    confidence = 0.4
    comment = "Mixed technical signals."

    if horizon == "short_term":
        if rsi is not None:
            if rsi < 30:
                signal = "Bullish"
                confidence = 0.65
                comment = "Oversold conditions suggest a possible short-term bounce."
            elif rsi > 70:
                signal = "Bearish"
                confidence = 0.65
                comment = "Overbought conditions increase short-term pullback risk."

    if horizon == "long_term":
        if "Uptrend" in trend:
            signal = "Bullish"
            confidence = 0.7
            comment = "Sustained trend strength supports long-term accumulation."
        elif "Downtrend" in trend:
            signal = "Bearish"
            confidence = 0.6
            comment = "Persistent weakness raises long-term risk."

    return {
        "signal": signal,
        "confidence": confidence,
        "comment": comment
    }
