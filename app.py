import streamlit as st
import openai
import pandas as pd
import requests
from datetime import datetime

# 🛠️ Setup
st.set_page_config(page_title="SMM Panel - BOP", layout="centered")
st.title("🚀 AI-Powered SMM Panel (BestOfPanel API)")

# ✅ Load API keys from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
bop_api_key = st.secrets["SMM_API_KEY"]
bop_api_url = "https://bestofpanel.com/api/v2"

# 🧪 Debug print to confirm API key is loaded (only shows partial for safety)
try:
    st.write("🔐 API key loaded (partial):", bop_api_key[:4] + "..." + bop_api_key[-4:])
except Exception as e:
    st.error("❌ API key not loaded from secrets.toml!")

# 💾 Order session
if "orders" not in st.session_state:
    st.session_state.orders = []

# 🧠 GPT Service Suggestion
st.subheader("🧠 Ask GPT for Suggestions")
user_input = st.text_input("Describe what you want:", placeholder="e.g. I want 1000 followers")

if user_input and st.button("🔍 Ask GPT"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"What SMM service fits this: '{user_input}'?"}]
        )
        suggestion = response['choices'][0]['message']['content']
        st.success(f"🤖 GPT Suggests: {suggestion}")
    except Exception as e:
        st.error(f"OpenAI Error: {e}")

# 📦 Define services with price (update IDs with real ones from your BOP panel)
services = {
    "Instagram Likes - ₹0.75/1K": (1010, 0.75),
    "Instagram Followers - ₹1.50/1K": (1020, 1.50),
    "YouTube Views - ₹0.60/1K": (1030, 0.60),
    "TikTok Likes - ₹0.80/1K": (1040, 0.80),
    "Instagram Reels Views - ₹0.70/1K": (1050, 0.70)
}

# 🧾 Order form
st.subheader("📦 Place an Order")
service_display = st.selectbox("Choose Service", list(services.keys()))
service_id, rate = services[service_display]
link = st.text_input("Target Link / Username")
quantity = st.slider("Quantity", 10, 10000, 100)
total_price = (quantity / 1000) * rate
st.markdown(f"💰 **Estimated Cost**: ₹{total_price:.2f}")

# ✅ Place order via BOP
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
            response = requests.post(bop_api_url, data=payload)
            result = response.json()
            if "order" in result:
                order_id = result["order"]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.orders.append({
                    "Time": timestamp,
                    "Service": service_display,
                    "Link": link,
                    "Quantity": quantity,
                    "Order ID": order_id,
                    "Cost (₹)": round(total_price, 2)
                })
                st.success(f"✅ Order Placed! ID: {order_id} | Cost: ₹{total_price:.2f}")
            else:
                st.error(f"❌ Error from BOP: {result}")
        except Exception as e:
            st.error(f"❌ API Call Failed: {e}")

# 📊 Order History
st.subheader("📊 Order History")
df = pd.DataFrame(st.session_state.orders)
if not df.empty:
    st.dataframe(df)
    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "orders.csv")
else:
    st.info("No orders yet.")
