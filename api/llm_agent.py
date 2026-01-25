# api/llm_agent.py

import os
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI

from api.tools.market import get_market_snapshot
from api.tools.ml import get_ml_outlook
from api.tools.news import get_company_news
from api.tools.risk import get_risk_metrics
from api.tools.charts import get_price_chart


# Load API key
def _get_api_key() -> str:
    """Loads OpenAI API key from key.txt or environment."""
    project_root = Path(__file__).parent.parent
    key_file = project_root / "key.txt"
    
    try:
        if key_file.exists():
            with open(key_file, "r") as f:
                return f.read().strip()
    except Exception:
        pass
    
    return os.getenv("OPENAI_API_KEY", "")


# Initialize OpenAI client
_client = None


def get_client() -> OpenAI:
    """Returns OpenAI client instance."""
    global _client
    if _client is None:
        api_key = _get_api_key()
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it in key.txt or OPENAI_API_KEY env var.")
        _client = OpenAI(api_key=api_key)
    return _client


# Enhanced system prompt for dynamic question handling
STOCKBOT_SYSTEM_PROMPT = """You are StockBot, an expert AI financial advisor and stock market analyst. You are highly knowledgeable, detailed, and adaptive when discussing stocks, investments, and market analysis.

**Key Capabilities:**
- Answer ANY stock-related question, even without specific ticker information
- Handle comparison questions (e.g., "Compare Apple and Microsoft")
- Provide general market insights and advice
- Analyze single stocks or multiple stocks
- Answer questions about market trends, sectors, or general investing

**Your Communication Style:**
- Be conversational, friendly, and professional (like ChatGPT)
- Provide detailed, comprehensive answers
- If you have real-time data, use it. If not, provide general insights based on your knowledge
- Explain complex financial concepts clearly
- Be adaptive to user's knowledge level
- Format responses with clear sections, bullet points, and emojis for readability
- Always include relevant numbers, percentages, and metrics when available

**Guidelines:**
- You can answer questions even if specific ticker data isn't available
- Use the provided data when available, but don't require it
- For comparison questions, analyze each stock mentioned
- Provide actionable insights, not just raw data
- Consider both short-term and long-term perspectives when relevant
- Mention risk factors and market conditions
- Be balanced - don't be overly bullish or bearish without data support
- If asked to compare stocks, provide a structured comparison

**Important:** You can handle ANY stock-related question, whether or not ticker data is provided. Use your knowledge and the available data to provide the best possible answer."""


def _fetch_stock_data(ticker: str, company: str) -> Dict:
    """Fetches all available data for a stock."""
    try:
        market = get_market_snapshot(ticker) or {}
        ml = get_ml_outlook(ticker) or {}
        news_data = get_company_news(company) or {}
        risk = get_risk_metrics(ticker) or {}
        chart = get_price_chart(ticker) or {}
        
        # Ensure news is a dict
        if isinstance(news_data, list):
            news = {"headlines": news_data, "sentiment": "Neutral"}
        else:
            news = news_data
        
        return {
            "ticker": ticker,
            "company": company,
            "market": market,
            "ml": ml,
            "news": news,
            "risk": {
                "level": risk.get("level", "Medium"),
                "volatility": risk.get("volatility"),
                "beta": risk.get("beta"),
                "max_drawdown": risk.get("max_drawdown"),
                "risk_score": risk.get("risk_score", 0.5)
            },
            "chart": chart if chart.get("available") else None
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "company": company,
            "error": str(e)
        }


def _format_stock_data_for_fallback(stock_data: Dict) -> str:
    """Formats stock data for fallback response (no LLM)."""
    if "error" in stock_data:
        return f"**{stock_data['company']} ({stock_data['ticker']}):** Data unavailable\n"
    
    parts = [f"## 📊 {stock_data['company']} ({stock_data['ticker']})\n"]
    
    market = stock_data.get("market", {})
    if market and market.get("price") is not None:
        change_str = ""
        if market.get("change_pct") is not None:
            sign = "+" if market.get("change", 0) >= 0 else ""
            change_str = f" ({sign}{market.get('change_pct', 0):.2f}%)"
        parts.append(f"**Current Price:** ${market.get('price', 0):.2f}{change_str}")
        if market.get("trend"):
            parts.append(f"**Trend:** {market.get('trend')}")
        parts.append("")
    
    ml = stock_data.get("ml", {})
    if ml:
        parts.append("### 🤖 ML/Technical Analysis")
        if ml.get("signal"):
            parts.append(f"- **Signal:** {ml.get('signal')}")
        if ml.get("confidence") is not None:
            parts.append(f"- **Confidence:** {ml.get('confidence', 0)*100:.1f}%")
        if ml.get("comment"):
            parts.append(f"- **Insight:** {ml.get('comment')}")
        parts.append("")
    
    risk = stock_data.get("risk", {})
    if risk:
        parts.append("### ⚠️ Risk Assessment")
        if risk.get("level"):
            parts.append(f"- **Risk Level:** {risk.get('level')}")
        if risk.get("volatility") is not None:
            parts.append(f"- **Volatility:** {risk.get('volatility'):.2f}%")
        if risk.get("beta") is not None:
            parts.append(f"- **Beta:** {risk.get('beta'):.2f}")
        if risk.get("max_drawdown") is not None:
            parts.append(f"- **Max Drawdown:** {risk.get('max_drawdown'):.2f}%")
        parts.append("")
    
    news = stock_data.get("news", {})
    if news and news.get("headlines"):
        parts.append("### 📰 Recent News")
        if news.get("sentiment"):
            parts.append(f"**Sentiment:** {news.get('sentiment')}")
        parts.append("**Headlines:**")
        for headline in news.get("headlines", [])[:5]:
            parts.append(f"- {headline}")
        parts.append("")
    
    return "\n".join(parts)


def _generate_fallback_response(user_message: str, stock_data_list: List[Dict]) -> str:
    """Generates a response without LLM when OpenAI is unavailable."""
    parts = []
    
    # Analyze the question type
    user_lower = user_message.lower()
    
    if any(word in user_lower for word in ["compare", "comparison", "vs", "versus", "difference"]):
        parts.append("## 📊 Stock Comparison\n")
        parts.append("Here's a comparison of the stocks you mentioned:\n")
    elif any(word in user_lower for word in ["risk", "risky", "safe", "volatility"]):
        parts.append("## ⚠️ Risk Analysis\n")
    elif any(word in user_lower for word in ["invest", "buy", "should i", "recommendation"]):
        parts.append("## 💡 Investment Analysis\n")
        parts.append("**Note:** This is informational only, not financial advice. Always do your own research.\n")
    else:
        parts.append("## 📈 Stock Analysis\n")
    
    # Add data for each stock
    for stock_data in stock_data_list:
        parts.append(_format_stock_data_for_fallback(stock_data))
    
    # Add disclaimer
    parts.append("---")
    parts.append("⚠️ **Note:** This analysis is based on available market data. For detailed insights, please ensure your OpenAI API quota is available.")
    
    return "\n".join(parts)


def generate_llm_response_dynamic(
    user_message: str,
    conversation_history: List[Dict[str, str]],
    resolved_stocks: List[Dict[str, str]]
) -> tuple:
    """
    Generates a dynamic, ChatGPT-like response that handles ANY stock question.
    Falls back to data-only response if OpenAI is unavailable.
    
    Returns:
        (response_text, meta_dict)
    """
    
    # Fetch data for all mentioned stocks
    stock_data_list = []
    for stock in resolved_stocks:
        data = _fetch_stock_data(stock["ticker"], stock["company"])
        stock_data_list.append(data)
    
    # Try to use OpenAI LLM
    try:
        client = get_client()
        
        # Format all stock data as context
        context_parts = []
        if stock_data_list:
            context_parts.append("# Available Stock Data\n")
            for stock_data in stock_data_list:
                if "error" not in stock_data:
                    context_parts.append(f"## {stock_data['company']} ({stock_data['ticker']})\n")
                    market = stock_data.get("market", {})
                    if market and market.get("price") is not None:
                        change_str = ""
                        if market.get("change_pct") is not None:
                            sign = "+" if market.get("change", 0) >= 0 else ""
                            change_str = f" ({sign}{market.get('change_pct', 0):.2f}%)"
                        context_parts.append(f"- Current Price: ${market.get('price', 0):.2f}{change_str}")
                    if market.get("trend"):
                        context_parts.append(f"- Trend: {market.get('trend')}")
                    ml = stock_data.get("ml", {})
                    if ml.get("signal"):
                        context_parts.append(f"- ML Signal: {ml.get('signal')}")
                    risk = stock_data.get("risk", {})
                    if risk.get("level"):
                        context_parts.append(f"- Risk Level: {risk.get('level')}")
                    context_parts.append("")
        
        data_context = "\n".join(context_parts) if context_parts else "No specific stock data available."
        
        # Build messages for the LLM
        messages = [
            {"role": "system", "content": STOCKBOT_SYSTEM_PROMPT},
        ]
        
        # Add conversation history (last 10 messages)
        for msg in conversation_history[-10:]:
            messages.append(msg)
        
        # Add current context
        if stock_data_list:
            messages.append({
                "role": "system",
                "content": f"Available stock data:\n\n{data_context}\n\nUse this data to provide a detailed, comprehensive answer to the user's question. If the question asks for a comparison, compare all mentioned stocks."
            })
        else:
            messages.append({
                "role": "system",
                "content": f"User question: {user_message}\n\nAnswer this question using your knowledge. You can provide general insights, market analysis, or advice even without specific ticker data."
            })
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Prepare metadata
        meta = {
            "intent": "general",
            "stocks_analyzed": [s["ticker"] for s in stock_data_list] if stock_data_list else [],
            "chart": stock_data_list[0].get("chart") if stock_data_list and stock_data_list[0].get("chart") else None
        }
        
        return response_text, meta
    
    except Exception as e:
        error_str = str(e)
        
        # Check if it's a quota/API error
        if "429" in error_str or "quota" in error_str.lower() or "insufficient_quota" in error_str.lower():
            # Use fallback response with available data
            if stock_data_list:
                fallback = _generate_fallback_response(user_message, stock_data_list)
                fallback += "\n\n⚠️ **Note:** OpenAI API quota exceeded. Showing data-based analysis. For AI-powered insights, please check your OpenAI billing."
            else:
                fallback = f"""I understand you're asking: **{user_message}**

However, I'm currently unable to access AI-powered responses due to API quota limits. 

**To get detailed analysis:**
- Check your OpenAI API billing and quota
- Or ask about a specific stock ticker for data-based insights

**Available stock data tools:**
- Real-time prices and trends
- Risk metrics (volatility, beta, drawdown)
- ML/technical analysis signals
- News sentiment"""
        else:
            # Other errors - use fallback with data if available
            if stock_data_list:
                fallback = _generate_fallback_response(user_message, stock_data_list)
                fallback += f"\n\n⚠️ **Note:** AI response unavailable (Error: {error_str[:100]}). Showing data-based analysis."
            else:
                fallback = f"""I encountered an error while processing your question.

**Your question:** {user_message}

**Error:** {error_str[:200]}

Please try rephrasing your question or ask about a specific stock ticker."""
        
        return fallback, {
            "error": error_str,
            "stocks_analyzed": [s["ticker"] for s in stock_data_list] if stock_data_list else [],
            "chart": stock_data_list[0].get("chart") if stock_data_list and stock_data_list[0].get("chart") else None
        }
