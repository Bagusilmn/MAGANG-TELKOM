import streamlit as st
import streamlit as st
# import pandas as pd
# import numpy as np
import os as os
from mapecocontro import *
from chatbot_controller_eco import load_chatbot, get_chatbot_response

gdf = map_path()
kecamatanList = kecamatan_list()
productlist = ["semua product", "Indihome", "By.u"]

# Selectbox For Kecamatan and Desa
colKecamatan, colProduct, colEmpty = st.columns([0.25, 0.25, 0.5])
with colKecamatan:
    selected_kecamatan = st.selectbox("Pilih Kecamatan",["Semua"] + kecamatanList, index=0, key="kecamatan")
with colProduct:
    selected_Product = st.selectbox("Pilih product", ["Semua"] + productlist, index=0, key="product")

# Div For Map and Recomendation
colMap, colText = st.columns([0.65, 0.35])
with colMap :
    map(st.session_state['kecamatan'])
    index_kecamatan = kecamatanList.index(st.session_state.get("kecamatan"))
with colText :
    # ==== Chatbot Produk Telkomsel ====
    with st.container(border=True, height=600):
        st.title(f"kec. {selected_kecamatan}")
        st.caption("Rekomendasi")

        # query = f"Berikan rekomendasi pilihan paket internet pada {selected_Product} di kecamatan {selected_kecamatan} berdasarkan jumlah penduduk, pendidikan dan pekerjaan yang ada disitu, dan berikan alasannya"
        query = f"Bagaimana strategi pemasaran yang cocok untuk diterapkan di wilayah kecamatan {selected_kecamatan} berdasarkan tingkat ekonomi dan dengan pendapatan masyarakat yang ada disitu, dan berikan alasannya"
        qa = load_chatbot()

        if query:
            with st.spinner("SSABAR SUMPAHH RODOK LEMOTTTT"):
                result = get_chatbot_response(qa, query)

                # st.markdown("### 🧠 ini dia jawabannya gesss:")
                st.markdown(result["result"])