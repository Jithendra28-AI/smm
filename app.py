import streamlit as st
import openai
import pandas as pd
import requests
from datetime import datetime

# Streamlit setup
st.set_page_config(page_title="SMM Panel (BOP)", layout="centered")
st.title("🚀 AI-Powered SMM Panel (BestOfPanel API)")

# Load secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
bop_api_key = st.secrets["SMM_API_KEY"]
bop_api_url = "https://bestofpanel.com/api/v2"  # Replace if different

# Session state to track orders
if "orders" not in st.session_state:
    st.session_state.orders = []

# 🧠 GPT Service Suggestion
st.subheader("🧠 Ask GPT to Suggest a Service")
user_input = st.text_input("What do you want?", placeholder="e.g. I want 500 Instagram followers fast")

if user_input and st.button("🔍 Ask GPT"):
    prompt = f"User request: {user_input}\nWhich SMM service fits best? Options: Instagram Likes, Instagram Followers, YouTube Views, TikTok Likes"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        suggestion = response['choices'][0]['message']['content']
        st.success(f"🤖 GPT Suggests: {suggestion}")
    except Exception as e:
        st.error(f"OpenAI Error: {e}")

# 💼 Define BOP service IDs (replace with your real IDs from BestOfPanel)
# Display name: (service ID, rate per 1K)
services = {
    "Instagram Likes [BOP] - ₹0.75/1K": (1010, 0.75),
    "Instagram Followers [BOP] - ₹1.50/1K": (1020, 1.50),
    "YouTube Views [BOP] - ₹0.60/1K": (1030, 0.60),
    "TikTok Likes [BOP] - ₹0.80/1K": (1040, 0.80),
    "Instagram Reels Views [BOP] - ₹0.70/1K": (1050, 0.70)
}


# 📦 Order Placement
st.subheader("📦 Place an Order")
service_name = st.selectbox("Choose Service", list(services.keys()))
service_id = services[service_name]
link = st.text_input("Target Link / Username")
quantity = st.slider("Quantity", 10, 10000, 100)

if st.button("✅ Submit Order"):
    if not link:
        st.warning("Please enter a valid link or username.")
    else:
        payload = {
            "key": bop_api_key,
            "action": "add",
            "service": service_id,
            "link": link,
            "quantity": quantity
        }
        try:
            res = requests.post(bop_api_url, data=payload)
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
                st.error(f"❌ Error from BOP: {result}")
        except Exception as e:
            st.error(f"❌ API Error: {e}")

# 📊 Show Order History
st.subheader("📊 Order History")
df = pd.DataFrame(st.session_state.orders)
if not df.empty:
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "orders.csv")
else:
    st.info("No orders placed yet.")
