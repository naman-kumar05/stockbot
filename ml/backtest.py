import numpy as np
import joblib
import yfinance as yf
from sklearn.metrics import mean_absolute_error, mean_squared_error

from ml.features import add_features
from ml.train import train

MODEL_DIR = "models/trained_models"


def backtest(ticker: str, test_size: float = 0.2):
    ticker = ticker.upper()

    # 1️⃣ Download historical data ONCE
    df = yf.download(
        ticker,
        start="2015-01-01",
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data found for {ticker}")

    df = add_features(df)

    # 2️⃣ Train once (or reuse model)
    train(ticker)
    model = joblib.load(f"{MODEL_DIR}/{ticker}.pkl")

    # 3️⃣ Train / test split
    split = int(len(df) * (1 - test_size))
    test_df = df.iloc[split:]

    y_true = []
    y_pred = []
    direction_hits = 0

    # 4️⃣ Walk forward through test data
    for i in range(1, len(test_df)):
        prev_price = test_df["Close"].iloc[i - 1].item()
        actual_price = test_df["Close"].iloc[i].item()

        features = test_df.drop("Close", axis=1).iloc[i - 1:i]
        predicted_price = model.predict(features).item()

        y_true.append(actual_price)
        y_pred.append(predicted_price)

        actual_up = actual_price > prev_price
        predicted_up = predicted_price > prev_price

        if actual_up == predicted_up:
            direction_hits += 1

    # 5️⃣ Metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    directional_accuracy = direction_hits / len(y_true)

    return {
        "ticker": ticker,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "directional_accuracy": round(directional_accuracy * 100, 2),
        "samples_tested": len(y_true)
    }
