import os
import joblib
import yfinance as yf
from xgboost import XGBRegressor
from ml.features import add_features

MODEL_DIR = "models/trained_models"
os.makedirs(MODEL_DIR, exist_ok=True)


def train(ticker: str):
    ticker = ticker.upper()
    print(f"Training model for {ticker}...")

    df = yf.download(ticker, start="2018-01-01", auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data found for ticker {ticker}")

    df = add_features(df)

    X = df.drop("Close", axis=1)
    y = df["Close"]

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    model.fit(X, y)

    model_path = f"{MODEL_DIR}/{ticker}.pkl"
    joblib.dump(model, model_path)

    print(f"Model saved at {model_path}")
