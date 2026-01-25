import feedparser
from urllib.parse import quote_plus

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

def get_company_news(company: str, limit=5):
    # URL encode the company name to handle spaces and special characters
    encoded_company = quote_plus(company)
    try:
        feed = feedparser.parse(
            f"https://news.google.com/rss/search?q={encoded_company}+stock"
        )
    except Exception as e:
        # Return empty news if feed parsing fails
        return {
            "sentiment": "Neutral",
            "headlines": []
        }

    headlines = []
    sentiments = []

    for entry in feed.entries[:limit]:
        headlines.append(entry.title)
        if HAS_TEXTBLOB:
            try:
                sentiment = TextBlob(entry.title).sentiment.polarity
                sentiments.append(sentiment)
            except:
                pass

    if HAS_TEXTBLOB and sentiments:
        avg_sentiment = sum(sentiments)/len(sentiments)
        sentiment_label = "Bullish" if avg_sentiment > 0.1 else "Bearish" if avg_sentiment < -0.1 else "Neutral"
    else:
        sentiment_label = "Neutral"

    return {
        "sentiment": sentiment_label,
        "headlines": headlines
    }
