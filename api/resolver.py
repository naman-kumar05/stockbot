# api/resolver.py

import re
import requests
from typing import Optional, Dict

YAHOO_SEARCH_URL = "https://query2.finance.yahoo.com/v1/finance/search"

STOPWORDS = {
    "stock", "share", "price", "analysis", "tell", "about",
    "company", "investment", "invest", "buy", "sell", "hold",
    "good", "bad", "should", "i", "is", "are", "the", "long",
    "term", "short", "future", "risk", "safe"
}


def _clean_query(text: str) -> str:
    """
    Cleans natural language into a Yahoo-searchable company string.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    tokens = [
        t for t in text.split()
        if t not in STOPWORDS and len(t) > 1
    ]

    return " ".join(tokens)


def resolve_company(
    user_message: str,
    fallback: Optional[str] = None
) -> Optional[Dict]:
    """
    Resolves a company name from natural language to a valid stock ticker.

    Returns:
    {
        "ticker": "AAPL",
        "company": "Apple Inc",
        "exchange": "NMS",
        "confidence": 0.82
    }
    """

    query = _clean_query(user_message)

    # Follow-up case: reuse last known ticker
    if not query and fallback:
        return {
            "ticker": fallback,
            "company": fallback,
            "exchange": None,
            "confidence": 0.5
        }

    if not query:
        return None

    try:
        response = requests.get(
            YAHOO_SEARCH_URL,
            params={
                "q": query,
                "quotesCount": 6,
                "newsCount": 0
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

    except Exception:
        return None

    quotes = data.get("quotes", [])

    # Keep only tradable equities / ETFs
    valid = [
        q for q in quotes
        if q.get("quoteType") in {"EQUITY", "ETF"}
        and q.get("symbol")
    ]

    if not valid:
        return None

    best = valid[0]

    return {
        "ticker": best.get("symbol"),
        "company": best.get("shortname") or best.get("longname"),
        "exchange": best.get("exchange"),
        "confidence": round(best.get("score", 0.5), 2)
    }


def resolve_company_to_ticker(user_message: str, fallback: Optional[str] = None) -> Dict:
    """
    Alias for resolve_company that returns a dict with 'success' key for compatibility.
    """
    result = resolve_company(user_message, fallback)
    
    if result is None:
        return {"success": False}
    
    return {
        "success": True,
        "ticker": result["ticker"],
        "name": result["company"],
        "exchange": result.get("exchange"),
        "confidence": result.get("confidence", 0.5)
    }
