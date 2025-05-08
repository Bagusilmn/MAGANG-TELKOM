import streamlit as st
import requests

st.title("Streamlit & Flask Integration")

# Panggil API Flask
response = requests.get("http://127.0.0.1:5000//debug_session")
if response.status_code == 200:
    data = response.json()
    st.write(data["User ID in session"])
else:
    st.error("Failed to fetch data from Flask API")