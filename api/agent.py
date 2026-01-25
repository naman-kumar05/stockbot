# api/agent.py

from api.memory import get_memory
from api.llm_agent import generate_llm_response_dynamic
from api.resolver import resolve_company_to_ticker


def chat_agent(user_message: str) -> dict:
    """
    ChatGPT-like conversational stock intelligence.
    No ticker resolution required - handles any question dynamically.
    """

    memory = get_memory()

    # -----------------------------
    # 1️⃣ EXTRACT TICKERS FROM QUESTION (OPTIONAL)
    # -----------------------------
    # Try to identify tickers mentioned, but don't fail if none found
    # The LLM will handle the question regardless
    
    mentioned_tickers = []
    mentioned_companies = []
    
    # Try to extract tickers/companies from the message
    # This is optional - the LLM can work without it
    words = user_message.split()
    
    # Common ticker patterns (1-5 uppercase letters)
    import re
    potential_tickers = re.findall(r'\b[A-Z]{1,5}\b', user_message)
    
    # Try to resolve company names mentioned
    resolved_data = []
    for word in words:
        if len(word) > 3:  # Skip short words
            resolved = resolve_company_to_ticker(word)
            if resolved.get("success"):
                ticker = resolved["ticker"]
                company = resolved["name"]
                if ticker not in [t["ticker"] for t in resolved_data]:
                    resolved_data.append({
                        "ticker": ticker,
                        "company": company
                    })
    
    # Also check for common company names (handles "Apple and Microsoft" type questions)
    company_keywords = {
        "apple": ("AAPL", "Apple Inc."),
        "microsoft": ("MSFT", "Microsoft Corporation"),
        "tesla": ("TSLA", "Tesla Inc."),
        "amazon": ("AMZN", "Amazon.com Inc."),
        "google": ("GOOGL", "Alphabet Inc."),
        "meta": ("META", "Meta Platforms Inc."),
        "facebook": ("META", "Meta Platforms Inc."),
        "nvidia": ("NVDA", "NVIDIA Corporation"),
        "netflix": ("NFLX", "Netflix Inc."),
        "disney": ("DIS", "The Walt Disney Company"),
        "jpmorgan": ("JPM", "JPMorgan Chase & Co."),
        "jpm": ("JPM", "JPMorgan Chase & Co."),
        "bank of america": ("BAC", "Bank of America Corp."),
        "bofa": ("BAC", "Bank of America Corp."),
        "visa": ("V", "Visa Inc."),
        "mastercard": ("MA", "Mastercard Inc."),
        "intel": ("INTC", "Intel Corporation"),
        "amd": ("AMD", "Advanced Micro Devices"),
        "ibm": ("IBM", "International Business Machines"),
        "oracle": ("ORCL", "Oracle Corporation"),
        "salesforce": ("CRM", "Salesforce Inc."),
        "adobe": ("ADBE", "Adobe Inc."),
        "paypal": ("PYPL", "PayPal Holdings Inc."),
        "uber": ("UBER", "Uber Technologies Inc."),
        "lyft": ("LYFT", "Lyft Inc."),
        "spotify": ("SPOT", "Spotify Technology"),
    }
    
    user_lower = user_message.lower()
    for keyword, (ticker, company) in company_keywords.items():
        if keyword in user_lower:
            if ticker not in [t["ticker"] for t in resolved_data]:
                resolved_data.append({
                    "ticker": ticker,
                    "company": company
                })
    
    # If no tickers found, that's okay - LLM will handle it
    if not resolved_data and memory.last_ticker:
        # Use last ticker from memory as context
        resolved_data.append({
            "ticker": memory.last_ticker,
            "company": memory.last_company or memory.last_ticker
        })

    # -----------------------------
    # 2️⃣ UPDATE MEMORY
    # -----------------------------
    
    memory.update(user_message=user_message)
    
    if resolved_data:
        memory.update(
            company=resolved_data[0]["company"],
            ticker=resolved_data[0]["ticker"]
        )

    # -----------------------------
    # 3️⃣ GENERATE DYNAMIC LLM RESPONSE
    # -----------------------------
    # The LLM will analyze the question and use available data
    
    conversation_history = memory.get_conversation_history()
    
    try:
        response_text, meta = generate_llm_response_dynamic(
            user_message=user_message,
            conversation_history=conversation_history,
            resolved_stocks=resolved_data  # Can be empty list
        )
        
        # Update memory with assistant response
        memory.update(assistant_message=response_text)
        
        return {
            "reply": response_text,
            "meta": meta
        }
    
    except Exception as e:
        # Fallback response
        error_response = f"""I apologize, but I encountered an error while processing your question.

**Your question:** {user_message}

**Error:** {str(e)}

Please try rephrasing your question or ask about a specific stock or company."""
        
        memory.update(assistant_message=error_response)
        
        return {
            "reply": error_response,
            "meta": {
                "error": str(e)
            }
        }
