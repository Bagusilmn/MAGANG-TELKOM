import streamlit as st
from model.rag_model import initialize_rag

@st.cache_resource
def load_model():
    return initialize_rag()

def build_question(kecamatan, desa, produk):
    return f"Berikan rekomendasi pilihan paket internet {produk} pada kecamatan {kecamatan} desa {desa} berdasarkan jumlah penduduk, pendidikan dan pekerjaan yang ada disitu, dan berikan alasannya"
    
def handle_question(qa_model, question):
    with st.spinner("SABAR SUMPAHH RODOK LEMOTTTT"):
        return qa_model(question)