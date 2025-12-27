import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="StockBot AI", page_icon="📈")
st.title("📈 StockBot AI")
st.write("Ask about stocks (AAPL, TSLA) or ask for **top 5 stocks**")

user_input = st.text_input(
    "You:",
    placeholder="What should I do with AAPL? or Tell me top 5 stocks"
)

if st.button("Ask"):
    if not user_input.strip():
        st.warning("Please enter a question.")
        st.stop()

    # 1️⃣ Call backend safely
    try:
        res = requests.post(
            API_URL,
            json={"message": user_input},
            timeout=15
        )
    except Exception as e:
        st.error("❌ Could not connect to backend. Is FastAPI running?")
        st.text(str(e))
        st.stop()

    # 2️⃣ Handle HTTP errors
    if res.status_code != 200:
        st.error(f"❌ Backend error ({res.status_code})")
        st.text(res.text)
        st.stop()

    # 3️⃣ Parse JSON safely
    try:
        data = res.json()
    except Exception:
        st.error("❌ Backend returned invalid JSON.")
        st.text(res.text)
        st.stop()

    # 4️⃣ API-level error
    if "error" in data:
        st.error(data["error"])
        st.stop()

    # 🔹 TOP STOCKS RESPONSE
    if data.get("type") == "top_stocks":
        st.subheader("🔥 Top 5 Stocks by Predicted Upside")

        for stock in data["stocks"]:
            st.markdown(
                f"""
                **{stock['ticker']}**  
                Current: ${stock['current_price']}  
                Predicted: ${stock['predicted_price']}  
                Expected Change: **{stock['expected_change_pct']}%**  
                Signal: **{stock['signal']}**
                ---
                """
            )

    # 🔹 SINGLE STOCK RESPONSE
    else:
        result = data["data"]

        st.subheader(f"📊 {result['ticker']} Analysis")
        st.write(f"**Current Price:** ${result['current_price']}")
        st.write(f"**Predicted Price:** ${result['predicted_price']}")
        st.write(f"**Expected Change:** {result['expected_change_pct']}%")

        if result["signal"] == "BUY":
            st.success("🟢 BUY")
        elif result["signal"] == "SELL":
            st.error("🔴 SELL")
        else:
            st.info("🟡 HOLD")

        st.write("🧠 **Explanation:**")
        st.write(data.get("explanation", ""))
