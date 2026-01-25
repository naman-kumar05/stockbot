# api/nlp.py

from typing import Dict, Optional

# -----------------------------
# Keyword banks
# -----------------------------

BUY_WORDS = {"buy", "invest", "enter", "accumulate"}
SELL_WORDS = {"sell", "exit", "dump", "book"}
HOLD_WORDS = {"hold", "wait", "stay"}
RISK_WORDS = {"risk", "safe", "volatile", "dangerous"}
FORECAST_WORDS = {"target", "forecast", "prediction", "price"}
NEWS_WORDS = {"news", "headline", "update", "announcement"}

LONG_TERM_WORDS = {
    "long term", "long-term", "5 years", "10 years",
    "future", "fundamentals"
}

SHORT_TERM_WORDS = {
    "short term", "short-term", "today", "tomorrow",
    "this week", "swing", "intraday"
}

UNCERTAIN_WORDS = {"maybe", "not sure", "confused", "uncertain"}
STRONG_WORDS = {"definitely", "strongly", "sure", "confident"}

FOLLOWUP_TRIGGERS = {
    "is it", "what about", "and", "should i",
    "risk", "long term", "safe"
}

# -----------------------------
# NLP Analyzer
# -----------------------------

def analyze_user_message(
    message: str,
    last_ticker: Optional[str] = None
) -> Dict:
    """
    Lightweight NLP engine.
    Returns intent, horizon, confidence, and follow-up detection.
    """

    text = message.lower()

    # Defaults
    intent = "overview"
    horizon = "short_term"
    confidence = "medium"
    is_followup = False

    # -----------------------------
    # Intent detection
    # -----------------------------

    if any(w in text for w in BUY_WORDS):
        intent = "buy"
    elif any(w in text for w in SELL_WORDS):
        intent = "sell"
    elif any(w in text for w in HOLD_WORDS):
        intent = "hold"
    elif any(w in text for w in RISK_WORDS):
        intent = "risk"
    elif any(w in text for w in FORECAST_WORDS):
        intent = "forecast"
    elif any(w in text for w in NEWS_WORDS):
        intent = "news"
    else:
        intent = "overview"

    # -----------------------------
    # Time horizon
    # -----------------------------

    if any(w in text for w in LONG_TERM_WORDS):
        horizon = "long_term"
    elif any(w in text for w in SHORT_TERM_WORDS):
        horizon = "short_term"

    # -----------------------------
    # Confidence level
    # -----------------------------

    if any(w in text for w in UNCERTAIN_WORDS):
        confidence = "low"
    elif any(w in text for w in STRONG_WORDS):
        confidence = "high"

    # -----------------------------
    # Follow-up detection
    # -----------------------------

    if last_ticker:
        if any(p in text for p in FOLLOWUP_TRIGGERS):
            is_followup = True

    return {
        "intent": intent,
        "horizon": horizon,
        "confidence": confidence,
        "is_followup": is_followup,
        "raw_text": message
    }
