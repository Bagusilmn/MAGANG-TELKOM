import streamlit as st

# def render_header():
#     st.set_page_config(page_title="ChatBot Produk Telkomsel", layout="centered")
#     st.title("🤖 Chatbot telkom euy punya chatbot euy")
#     st.caption("Powered by TRALALA AI")



# def input_user_query():
#     return st.text_input("takok opo ae iso pokok ga takok bejo")

def location_selector(kecamatan_list, desa_list):
    selected_kecamatan = st.selectbox("Pilih Kecamatan", kecamatan_list)
    selected_desa = st.selectbox("Pilih Desa", desa_list)
    # selected_product = st.selectbox("product", product_list)
    return selected_kecamatan, selected_desa

def product_selector(produk_list):
    selected_produk = st.selectbox("semua produk", produk_list)
    return selected_produk

def display_answer(result):
    st.markdown("### 🧠 ini dia jawabannya gesss:")
    st.markdown(result["result"])

# def display_sources(result):
#     st.markdown("---")
#     st.markdown("#### 📄 Dokumen yang dijadikan referensi:")
#     for i, doc in enumerate(result["source_documents"]):
#         st.markdown(f"**Dokumen {i+1}:**")
#         st.text(doc.page_content[:100] + "...")

