# 📈 StockBot AI

A ChatGPT-like AI assistant for stock market analysis, powered by OpenAI's LLM and real-time market data.

## Features

- **🤖 LLM-Powered Conversations**: Uses OpenAI GPT models for natural, adaptive responses
- **📊 Real-Time Market Data**: Fetches live stock prices, trends, and technical indicators
- **📰 News Sentiment Analysis**: Analyzes recent news and market sentiment
- **⚠️ Risk Assessment**: Calculates volatility, beta, drawdown, and risk metrics
- **📈 Technical Analysis**: Provides RSI, moving averages, support/resistance levels
- **💬 ChatGPT-like Interface**: Beautiful Streamlit UI with conversation history
- **🧠 Context-Aware**: Maintains conversation history for follow-up questions

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Place your OpenAI API key in `key.txt` in the project root, or set it as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run the Backend

**Important:** Run from the project root directory, not from inside the `api` folder!

```bash
# From project root:
uvicorn api.main:app --reload --port 8000
```

### 4. Run the Frontend

In a new terminal:

```bash
cd ui
streamlit run app.py
```

The UI will open in your browser at `http://localhost:8501`

## Usage

### Example Questions

- "What's the current price of Apple?"
- "Should I invest in Tesla?"
- "Analyze Microsoft's risk profile"
- "What's the news sentiment for NVIDIA?"
- "Compare Apple and Microsoft stocks"
- "What's the forecast for Amazon?"

### API Endpoints

- `POST /chat` - Send a message to StockBot
  ```json
  {
    "message": "What's the price of Apple?"
  }
  ```

- `POST /clear-history` - Clear conversation history
- `GET /health` - Health check

## Architecture

```
StockBot/
├── api/
│   ├── main.py          # FastAPI server
│   ├── agent.py         # Main agent orchestrator
│   ├── llm_agent.py     # LLM integration (OpenAI)
│   ├── memory.py        # Conversation memory
│   ├── nlp.py           # Intent detection
│   ├── resolver.py      # Company/ticker resolution
│   ├── response.py      # Fallback response builder
│   └── tools/
│       ├── market.py    # Market data (yfinance)
│       ├── ml.py        # ML/technical analysis
│       ├── news.py      # News sentiment
│       ├── risk.py      # Risk metrics
│       └── charts.py    # Chart data
└── ui/
    └── app.py           # Streamlit UI
```

## How It Works

1. **User Input**: User asks a question about stocks
2. **NLP Analysis**: System detects intent and extracts entities
3. **Ticker Resolution**: Resolves company names to stock tickers
4. **Data Collection**: Fetches market data, news, risk metrics, charts
5. **LLM Generation**: OpenAI LLM generates detailed, adaptive response
6. **Response**: Returns formatted response with charts and metrics

## Technologies

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4o-mini (configurable)
- **Market Data**: yfinance
- **News**: Google News RSS + TextBlob sentiment
- **Technical Analysis**: Custom RSI, moving averages, support/resistance

## Notes

⚠️ **Disclaimer**: This tool is for informational purposes only. It does not provide financial advice. Always do your own research before making investment decisions.

## License

MIT
