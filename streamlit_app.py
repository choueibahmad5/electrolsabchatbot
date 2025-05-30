
import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="ElectroSlab Smart Bot", layout="centered")

st.title("🤖 ElectroSlab Chatbot")
st.markdown("**اسأل عن أي منتج، والبوت بيجاوبك!**")

# Step 1: Get the API key
api_key = st.text_input("🔑 OpenAI API Key", type="password")

# Step 2: Load product data
try:
    df = pd.read_csv("electroslab_products.csv")
except:
    st.error("❌ ما قدرنا نقرأ ملف المنتجات. تأكد إنه موجود جنب ملف .py")

# Step 3: User Query
query = st.text_input("📝 شو بدك تسأل؟")

# Step 4: Search logic using GPT
def generate_reply(query, products, api_key):
    product_info = "\n".join(
        [f"{row['Product Name']} - {row['Price']} - {row['Link']}" for _, row in products.iterrows()]
    )
    prompt = f"""
    هاي لائحة منتجات إلكترونية:

    {product_info}

    زبون سأل: "{query}"

    جاوبو بشكل ذكي ومقنع، وإذا في منتج مناسب، قلّو الاسم، السعر والرابط.
    إذا ما في شي مناسب، قلّو برقة إنو مش متوفر.
    """

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"🚨 صار في مشكلة: {e}"

# Step 5: Show response
if st.button("أرسل السؤال") and query and api_key:
    reply = generate_reply(query, df, api_key)
    st.markdown(reply)
