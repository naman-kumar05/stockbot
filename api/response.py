# api/response.py

import random


# ----------------------------------
# Confidence label helper
# ----------------------------------

def _confidence_label(level: str) -> str:
    return {
        "high": "High",
        "medium": "Medium",
        "low": "Low"
    }.get(level, "Medium")


# ----------------------------------
# Reasoning templates (VARIABILITY)
# ----------------------------------

REASONING_BANK = {
    "buy": [
        "Momentum and supporting indicators suggest potential upside, but timing remains important.",
        "This setup could offer an entry opportunity, provided it aligns with your risk tolerance.",
        "Short-term conditions appear constructive, though confirmation is still developing."
    ],
    "sell": [
        "Upside momentum looks limited at current levels, which may justify profit protection.",
        "Risk-reward appears less favorable, especially if volatility increases.",
        "Reducing exposure could be reasonable if capital preservation is a priority."
    ],
    "hold": [
        "The stock is currently consolidating, making patience a sensible approach.",
        "There is no strong directional signal yet, suggesting a wait-and-watch stance.",
        "Holding allows you to observe how price reacts to upcoming market catalysts."
    ],
    "risk": [
        "Volatility and drawdown metrics indicate meaningful risk that should not be ignored.",
        "Market sensitivity suggests this stock may react sharply to broader index moves.",
        "Risk remains elevated under current conditions, especially for short-term positions."
    ],
    "general": [
        "Overall signals are mixed, reflecting a balance between opportunity and caution.",
        "The stock shows no extreme strength or weakness at this stage.",
        "Current conditions suggest neutrality rather than aggressive positioning."
    ],
    "long_term": [
        "From a long-term perspective, business fundamentals matter more than short-term price noise.",
        "Long-term investors should focus on competitive positioning and earnings durability.",
        "Structural growth drivers are more important here than near-term fluctuations."
    ]
}


# ----------------------------------
# Core response builder
# ----------------------------------

def build_response(
    company: str,
    ticker: str,
    intent: str,
    horizon: str,
    confidence: str,
    market: dict,
    ml: dict,
    news: dict,
    risk: dict
) -> str:
    """
    Converts structured data into a ChatGPT-like professional response.
    """

    confidence_text = _confidence_label(confidence)

    # ----------------------------------
    # Market Snapshot
    # ----------------------------------

    price = market.get("price")
    trend = market.get("trend")

    market_lines = []
    if price is not None:
        market_lines.append(f"• Current Price: {price:.2f}")
    if trend:
        market_lines.append(f"• Trend: {trend}")

    market_block = "\n".join(market_lines) if market_lines else "• Market data currently unavailable."

    # ----------------------------------
    # ML Outlook
    # ----------------------------------

    ml_signal = ml.get("signal", "Neutral")
    ml_comment = ml.get(
        "comment",
        "Model confidence is limited due to neutral price structure."
    )

    ml_block = (
        f"• ML Outlook ({horizon.replace('_', ' ').title()}): {ml_signal}\n"
        f"• ML Confidence: {_confidence_label(ml.get('confidence', 'low'))}\n"
        f"• Model Insight: {ml_comment}"
    )

    # ----------------------------------
    # News & Sentiment
    # ----------------------------------

    headlines = news.get("headlines", [])
    sentiment = news.get("sentiment", "Neutral")

    news_lines = [f"• Market Sentiment: {sentiment}"]

    if headlines:
        sample = random.sample(headlines, min(3, len(headlines)))
        news_lines.append("• Recent Headlines:")
        for h in sample:
            news_lines.append(f"  - {h}")

    news_block = "\n".join(news_lines)

    # ----------------------------------
    # Risk Assessment
    # ----------------------------------

    risk_level = risk.get("level", "Medium")
    volatility = risk.get("volatility")
    drawdown = risk.get("drawdown")

    risk_lines = [f"• Risk Level: {risk_level}"]

    if volatility is not None:
        risk_lines.append(f"• Volatility: {volatility:.2f}%")
    if drawdown is not None:
        risk_lines.append(f"• Max Drawdown: {drawdown:.2f}%")

    risk_block = "\n".join(risk_lines)

    # ----------------------------------
    # Reasoning (VARIABLE)
    # ----------------------------------

    reasoning_pool = REASONING_BANK.get(intent, REASONING_BANK["general"])
    reasoning = random.choice(reasoning_pool)

    # ----------------------------------
    # Final Assembly
    # ----------------------------------

    response = f"""
📊 **{company} ({ticker}) Analysis**

{market_block}

🤖 **AI Outlook**
{ml_block}

📰 **News & Sentiment**
{news_block}

⚠️ **Risk Assessment**
{risk_block}

🧠 **AI Reasoning**
{reasoning}

Confidence Level: **{confidence_text}**
""".strip()

    return response
