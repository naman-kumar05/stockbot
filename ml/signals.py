def get_signal(current_price: float, predicted_price: float) -> dict:


    change_pct = ((predicted_price - current_price) / current_price) * 100

    if change_pct >= 2:
        signal = "BUY"
    elif change_pct <= -2:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "signal": signal,
        "expected_change_pct": round(change_pct, 2)
    }
