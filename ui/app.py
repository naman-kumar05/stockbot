import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="StockBot AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-like appearance
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #f0f2f6;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #ffffff;
        margin-right: 20%;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #667eea;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #5568d3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_url" not in st.session_state:
    st.session_state.api_url = "http://127.0.0.1:8000"

# Title and description
st.title("📈 StockBot AI")
st.markdown("""
<div style='text-align: center; color: white; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 2rem;'>
    <h3>Your AI-Powered Stock Market Assistant</h3>
    <p>Ask me anything about stocks, companies, market analysis, risk assessment, and more!</p>
    <p style='font-size: 0.9em; opacity: 0.9;'>Powered by advanced LLM technology with real-time market data</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input("API URL", value=st.session_state.api_url)
    st.session_state.api_url = api_url
    
    if st.button("🗑️ Clear Chat History"):
        try:
            response = requests.post(
                f"{st.session_state.api_url}/clear-history",
                json={},
                timeout=5
            )
            st.session_state.messages = []
            st.success("Chat history cleared!")
            st.rerun()
        except Exception as e:
            st.error(f"Error clearing history: {e}")
    
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    example_questions = [
        "What's the current price of Apple?",
        "Should I invest in Tesla?",
        "Analyze Microsoft's risk profile",
        "What's the news sentiment for NVIDIA?",
        "Compare Apple and Microsoft stocks",
        "What's the forecast for Amazon?"
    ]
    
    for question in example_questions:
        if st.button(question, key=f"example_{question}", use_container_width=True):
            st.session_state.user_input = question
            st.rerun()

# Display chat history
chat_container = st.container()

with chat_container:
    for idx, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")
        
        if role == "user":
            with st.chat_message("user"):
                st.markdown(f"**You:** {content}")
                if timestamp:
                    st.caption(timestamp)
        else:
            with st.chat_message("assistant"):
                st.markdown(content)
                if timestamp:
                    st.caption(timestamp)
                
                # Display chart if available
                if "meta" in message and message["meta"].get("chart"):
                    chart_data = message["meta"]["chart"]
                    if chart_data and chart_data.get("available"):
                        st.subheader("📊 Price Chart")
                        df = pd.DataFrame(chart_data.get("chart", []))
                        if not df.empty:
                            df["date"] = pd.to_datetime(df["date"])
                            df.set_index("date", inplace=True)
                            st.line_chart(df[["close", "ma20", "ma50"]].dropna())
                            
                            # Display technical indicators
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Trend", chart_data.get("trend", "N/A"))
                            with col2:
                                st.metric("Support", f"${chart_data.get('support', 0):.2f}" if chart_data.get("support") else "N/A")
                            with col3:
                                st.metric("Resistance", f"${chart_data.get('resistance', 0):.2f}" if chart_data.get("resistance") else "N/A")

# Chat input
user_input = st.chat_input("Ask me about any stock or company...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(f"**You:** {user_input}")
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing market data and generating response..."):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/chat",
                    json={"message": user_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "I apologize, but I couldn't generate a response.")
                    
                    # Display response
                    st.markdown(reply)
                    
                    # Add assistant message to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "meta": data.get("meta", {})
                    })
                    
                    # Display chart if available
                    chart_data = data.get("meta", {}).get("chart")
                    if chart_data and chart_data.get("available"):
                        st.subheader("📊 Price Chart")
                        df = pd.DataFrame(chart_data.get("chart", []))
                        if not df.empty:
                            df["date"] = pd.to_datetime(df["date"])
                            df.set_index("date", inplace=True)
                            st.line_chart(df[["close", "ma20", "ma50"]].dropna())
                            
                            # Display technical indicators
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Trend", chart_data.get("trend", "N/A"))
                            with col2:
                                st.metric("Support", f"${chart_data.get('support', 0):.2f}" if chart_data.get("support") else "N/A")
                            with col3:
                                st.metric("Resistance", f"${chart_data.get('resistance', 0):.2f}" if chart_data.get("resistance") else "N/A")
                
                else:
                    error_msg = f"❌ Backend error (Status {response.status_code})"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
            
            except requests.exceptions.ConnectionError:
                error_msg = "❌ Could not connect to the API. Make sure the backend server is running on port 8000."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 1rem;'>
    <p>StockBot AI - Powered by OpenAI GPT & Real-time Market Data</p>
    <p style='font-size: 0.8em; opacity: 0.8;'>⚠️ This is for informational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
