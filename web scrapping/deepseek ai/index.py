import streamlit as st
import requests
import markdown

st.set_page_config(page_title="WSP ChatBot", layout="centered")

st.title("🤖 Free ChatBot")

user_input = st.text_input("Enter your question", "")

if st.button("Ask!") and user_input.strip():
    with st.spinner("Loading..."):
        try:
            headers = {
                "Authorization": "Bearer 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",
                "HTTP-Referer": "https://www.webstylepress.com",
                "X-Title": "webstylepress",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek/deepseek-r1:free",
                "messages": [{"role": "user", "content": user_input}]
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
            st.markdown(content)
        except Exception as e:
            st.error(f"Error: {e}")
