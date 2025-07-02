import streamlit as st
import openai
import pandas as pd
import requests
from datetime import datetime

# Streamlit page config
st.set_page_config(page_title="SMM Panel", layout="centered")
st.title("🚀 AI-Powered SMM Panel with JAP API")

# API keys from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
jap_api_key = st.secrets["SMM_API_KEY"]
jap_api_url = "https://justanotherpanel.com/api/v2"

# Order history (in session memory)
if "orders" not in st.session_state:
    st.session_state.orders = []

# Step 1: AI Suggestion
st.subheader("🧠 Ask AI to Suggest Service")
user_input = st.text_input("What do you need?", placeholder="I want 1000 followers on Instagram")
if user_input and st.button("🔍 Ask GPT"):
    prompt = f"User request: {user_input}\nWhat SMM service fits best? Choose from: Instagram Followers, YouTube Views, TikTok Likes"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        suggestion = response['choices'][0]['message']['content']
        st.success(f"🤖 GPT Suggests: {suggestion}")
    except Exception as e:
        st.error(f"OpenAI Error: {e}")

# Step 2: Place Order
st.subheader("📦 Place an Order")

# You should replace these with real service IDs from your JAP account
services = {
    "Instagram Followers (Real)": 101,  # replace with actual ID from your panel
    "YouTube Views": 102,
    "TikTok Likes": 103
}

service_name = st.selectbox("Select Service", list(services.keys()))
service_id = services[service_name]
link = st.text_input("Target Link / Username")
quantity = st.slider("Quantity", 10, 10000, 100)

if st.button("✅ Submit Order"):
    if not link:
        st.warning("Please enter a valid link or username.")
    else:
        payload = {
            "key": jap_api_key,
            "action": "add",
            "service": service_id,
            "link": link,
            "quantity": quantity
        }
        try:
            res = requests.post(jap_api_url, data=payload)
            result = res.json()
            if "order" in result:
                order_id = result["order"]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.orders.append({
                    "Time": timestamp,
                    "Service": service_name,
                    "Link": link,
                    "Quantity": quantity,
                    "Order ID": order_id
                })
                st.success(f"✅ Order Placed! Order ID: {order_id}")
            else:
                st.error(f"❌ Error from JAP: {result}")
        except Exception as e:
            st.error(f"❌ API Error: {e}")

# Step 3: Order History
st.subheader("📊 Order History")
df = pd.DataFrame(st.session_state.orders)
if not df.empty:
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "orders.csv")
else:
    st.info("No orders placed yet.")
