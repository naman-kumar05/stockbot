import pandas as pd
import ta

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    df["rsi"] = ta.momentum.RSIIndicator(close).rsi()
    df["macd"] = ta.trend.MACD(close).macd()
    df["sma_20"] = close.rolling(20).mean()
    df["sma_50"] = close.rolling(50).mean()
    df["volatility"] = close.pct_change().rolling(20).std()

    df.dropna(inplace=True)
    return df
