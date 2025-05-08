import streamlit as st
import streamlit as st
# import pandas as pd
# import numpy as np
import os as os
from mappopucontro import *
from chatbot_controller_popu import load_chatbot, get_chatbot_response

gdf = map_path()
kecamatanList = kecamatan_list()
desalist = desa_list()
productlist = ["semua product", "Indihome", "By.u"]

# Selectbox For Kecamatan and Desa
colKecamatan, colDesa, colProduct, colEmpty = st.columns([0.25, 0.25, 0.25, 0.5])
with colKecamatan:
    selected_kecamatan = st.selectbox("Pilih Kecamatan",["Semua"] + kecamatanList, index=0, key="kecamatan")
with colDesa:
    if selected_kecamatan != "Semua":
        desa_list = sorted(gdf[gdf['WADMKC'] == selected_kecamatan]['NAMOBJ'].unique())
    else:
        desa_list = sorted(gdf['NAMOBJ'].unique())
    selected_desa = st.selectbox("Pilih Desa", ["Semua"] + desalist, index=0, key="desa")
with colProduct:
    selected_Product = st.selectbox("Pilih product", ["Semua"] + productlist, index=0, key="product")

# Div For Map and Recomendation
colMap, colText = st.columns([0.65, 0.35])
with colMap :
    map(st.session_state['kecamatan'], st.session_state['desa'])
    index_kecamatan = kecamatanList.index(st.session_state.get("kecamatan"))
with colText :
    # ==== Chatbot Produk Telkomsel ====
    with st.container(border=True, height=600):
        st.title(f"kec. {selected_kecamatan} desa {selected_desa}")
        st.caption("Rekomendasi")

        # query = f"Berikan rekomendasi pilihan paket internet pada {selected_Product} di kecamatan {selected_kecamatan} desa {selected_desa} berdasarkan jumlah penduduk, pendidikan dan pekerjaan yang ada disitu, dan berikan alasannya"
        query = f"Berikan beberapa rekomendasi pilihan paket internet pada {selected_Product} di kecamatan {selected_kecamatan} desa {selected_desa} berdasarkan jumlah penduduk, pendidikan dan pekerjaan yang ada diwilayah tersebut, serta sesuai dengan tingkat ekonomi yang ada pada kecamatan {selected_kecamatan} dan berikan alasannya"
        qa = load_chatbot()

        if query:
            with st.spinner("SSABAR SUMPAHH RODOK LEMOTTTT"):
                result = get_chatbot_response(qa, query)

                # st.markdown("### 🧠 ini dia jawabannya gesss:")
                st.markdown(result["result"])