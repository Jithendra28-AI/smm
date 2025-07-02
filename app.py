import streamlit as st
import openai
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="SMM Panel", layout="centered")
st.title("🚀 AI-Powered SMM Panel")

# OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Dummy service list
services = {
    "Instagram Followers": 101,
    "YouTube Views": 102,
    "TikTok Likes": 103,
}

# Session state for orders
if "orders" not in st.session_state:
    st.session_state.orders = []

# Step 1: AI-Driven Service Detection
st.subheader("🧠 Ask AI to Suggest Service")
user_input = st.text_input("What do you need?", placeholder="I want 1000 followers on Instagram")
if user_input and st.button("🔍 Ask GPT"):
    prompt = f"User request: {user_input}\nWhat service is needed? Choose from: {list(services.keys())}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    suggestion = response['choices'][0]['message']['content']
    st.success(f"🤖 GPT Suggests: {suggestion}")

# Step 2: Manual Order Form
st.subheader("📦 Place an Order")
service = st.selectbox("Choose Service", list(services.keys()))
link = st.text_input("Enter Link / Username")
quantity = st.slider("Quantity", 10, 10000, 100)
if st.button("✅ Submit Order"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.orders.append({
        "Time": timestamp,
        "Service": service,
        "Link": link,
        "Quantity": quantity
    })
    st.success("✅ Order submitted (demo mode — no real API used)")

# Step 3: Order Log
st.subheader("📊 Order History")
df = pd.DataFrame(st.session_state.orders)
if not df.empty:
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "orders.csv")
else:
    st.info("No orders yet.")
