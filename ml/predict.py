import os
import joblib
import yfinance as yf
from ml.features import add_features
from ml.train import train

MODEL_DIR = "models/trained_models"


def predict_stock(ticker: str):
    model_path = os.path.join(MODEL_DIR, f"{ticker}.pkl")

    # 🔹 Train model if missing
    if not os.path.exists(model_path):
        train(ticker)

    # Load model
    model = joblib.load(model_path)

    # Download recent data
    df = yf.download(ticker, period="6mo")

    if df.empty:
        raise ValueError(f"No data found for {ticker}")

    df = add_features(df)
    df = df.dropna()

    X = df.drop(columns=["Close"])
    last_row = X.iloc[-1:]

    predicted_price = float(model.predict(last_row)[0])
    current_price = float(df["Close"].iloc[-1])

    expected_change_pct = round(
        ((predicted_price - current_price) / current_price) * 100,
        2
    )

    # Signal logic
    if expected_change_pct > 1:
        signal = "BUY"
    elif expected_change_pct < -1:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "predicted_price": round(predicted_price, 2),
        "expected_change_pct": expected_change_pct,
        "signal": signal,
    }
