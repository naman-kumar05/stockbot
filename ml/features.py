import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Simple moving averages
    df["ma_5"] = df["Close"].rolling(window=5).mean()
    df["ma_10"] = df["Close"].rolling(window=10).mean()

    # Momentum
    df["return_1"] = df["Close"].pct_change(1)
    df["return_5"] = df["Close"].pct_change(5)

    return df
