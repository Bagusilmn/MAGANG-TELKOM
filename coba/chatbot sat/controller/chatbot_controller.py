import streamlit as st
from model.rag_model import initialize_rag

@st.cache_resource
def load_model():
    return initialize_rag()

def build_question(kecamatan, desa):
    return f"Berikan rekomendasi pilihan paket internet pada kecamatan {kecamatan} desa {desa} dengan kepadatan penduduk yang ada disitu"
    
# def handle_question(qa_model, question):
#     if question:
#         with st.spinner("SABAR SUMPAHH RODOK LEMOTTTT"):
#             result = qa_model(question)
#             return result
#     return None

def handle_question(qa_model, question):
    with st.spinner("SABAR SUMPAHH RODOK LEMOTTTT"):
        return qa_model(question)