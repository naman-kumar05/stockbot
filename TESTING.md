# 🧪 Testing StockBot

This guide will help you test your StockBot application.

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify API key:**
   - Make sure `key.txt` exists in the project root with your OpenAI API key
   - Or set `OPENAI_API_KEY` environment variable

## Testing Methods

### Method 1: Automated Test Script (Recommended)

1. **Start the backend server (from project root):**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. **In a new terminal, run the test script:**
   ```bash
   python test_stockbot.py
   ```

   This will test:
   - ✅ Health endpoint
   - ✅ Chat functionality with multiple questions
   - ✅ Clear history endpoint

### Method 2: Manual API Testing with curl

1. **Start the backend (from project root):**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. **Test health endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test chat endpoint:**
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"What's the price of Apple?\"}"
   ```

4. **Test with PowerShell (Windows):**
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8000/chat" `
     -Method POST `
     -ContentType "application/json" `
     -Body '{"message": "What is the current price of Apple?"}'
   ```

### Method 3: UI Testing (Full Experience)

1. **Start the backend (from project root):**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

2. **Start the frontend (in a new terminal):**
   ```bash
   cd ui
   streamlit run app.py
   ```

3. **Or use the batch file:**
   ```bash
   start.bat
   ```

4. **Open your browser:**
   - Frontend: http://localhost:8501
   - Backend API docs: http://localhost:8000/docs

5. **Test in the UI:**
   - Type questions like:
     - "What's the current price of Apple?"
     - "Should I invest in Tesla?"
     - "Analyze Microsoft's risk profile"
     - "What's the news sentiment for NVIDIA?"
   - Check that responses are detailed and adaptive
   - Verify charts appear for valid tickers
   - Test follow-up questions (e.g., "What about its risk?")

### Method 4: Python Interactive Testing

```python
import requests

# Test health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test chat
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's the price of Apple?"}
)
print(response.json()["reply"])
```

## What to Test

### ✅ Core Functionality

- [ ] Backend server starts without errors
- [ ] Health endpoint returns 200
- [ ] Chat endpoint accepts messages
- [ ] LLM generates responses
- [ ] Market data is fetched correctly
- [ ] Ticker resolution works
- [ ] Charts are generated

### ✅ Conversation Features

- [ ] Follow-up questions work (e.g., ask about Apple, then "What about its risk?")
- [ ] Conversation history is maintained
- [ ] Clear history works
- [ ] Context is preserved across messages

### ✅ Data Quality

- [ ] Stock prices are current
- [ ] News sentiment is calculated
- [ ] Risk metrics are computed
- [ ] Technical indicators (RSI, MA) are shown
- [ ] Charts display correctly

### ✅ Error Handling

- [ ] Invalid tickers are handled gracefully
- [ ] Missing data shows appropriate messages
- [ ] API errors don't crash the app
- [ ] Network errors are handled

## Common Issues & Solutions

### Issue: "Could not connect to API"
**Solution:** Make sure the backend is running on port 8000

### Issue: "OpenAI API key not found"
**Solution:** 
- Check that `key.txt` exists in project root
- Or set `OPENAI_API_KEY` environment variable

### Issue: "Module not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: Slow responses
**Solution:** 
- This is normal - LLM calls take a few seconds
- Market data fetching also takes time
- Consider using a faster model (gpt-4o-mini is already fast)

### Issue: Charts not showing
**Solution:**
- Check that yfinance is working: `pip install yfinance --upgrade`
- Some tickers may not have chart data available

## Performance Testing

Test response times:
```python
import time
import requests

start = time.time()
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's the price of Apple?"}
)
elapsed = time.time() - start
print(f"Response time: {elapsed:.2f} seconds")
```

Expected: 3-10 seconds (depends on LLM and market data fetching)

## Integration Testing

Test the full flow:
1. Ask about a stock
2. Ask a follow-up question
3. Ask about a different stock
4. Clear history
5. Ask again (should not have context from before)

## Debugging

### Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check backend logs:
The uvicorn server will show request logs in the terminal

### Check API documentation:
Visit http://localhost:8000/docs for interactive API testing

## Next Steps

Once basic testing passes:
1. Test with various stock tickers
2. Test edge cases (invalid companies, very long messages)
3. Test concurrent requests
4. Monitor memory usage during long conversations
5. Test with different LLM models (edit `api/llm_agent.py`)
