import streamlit as st
import streamlit as st
# import pandas as pd
# import numpy as np
import os as os
from controller.mappopucontro import *
from controller.chatbot_controller import load_chatbot, get_chatbot_response

gdf = map_path()
kecamatanList = kecamatan_list()
desalist = desa_list()

# Selectbox For Kecamatan and Desa
colKecamatan, colDesa, colEmpty = st.columns([0.25, 0.25, 0.5])
with colKecamatan:
    selected_kecamatan = st.selectbox("Pilih Kecamatan", ["Search Kecamatan"] + ["Semua"] + kecamatanList, index=0, key="kecamatan")
with colDesa:
    if selected_kecamatan != "Semua":
        desa_list = sorted(gdf[gdf['WADMKC'] == selected_kecamatan]['NAMOBJ'].unique())
    else:
        desa_list = sorted(gdf['NAMOBJ'].unique())
    selected_desa = st.selectbox("Pilih Desa", ["Search Desa"] + ["Semua"] + desalist, index=0, key="desa")

# Div For Map and Recomendation
colMap, colText = st.columns([0.65, 0.35])
with colMap :
    map(st.session_state['kecamatan'], st.session_state['desa'])
    index_kecamatan = kecamatanList.index(st.session_state.get("kecamatan"))
with colText :
    # ==== Chatbot Produk Telkomsel ====
    st.title("🤖 ChatBot Produk Telkomsel (RAG)")
    st.caption("Powered by OpenRouter + LangChain + HuggingFace Embeddings")

    query = st.text_input("Tanyakan apa pun tentang IndiHome, Orbit, Telkomsel One, dll:")

    qa = load_chatbot()

    if query:
        with st.spinner("Sedang mencari jawaban..."):
            result = get_chatbot_response(qa, query)

            st.markdown("### 🧠 Jawaban:")
            st.markdown(result["result"])