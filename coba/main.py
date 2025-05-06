import os
from controller.chatbot_controller import load_model, handle_question, build_question
from view.chatbot_view import display_answer,  location_selector, product_selector

# ===== Set API Key =====
# os.environ["OPENAI_API_KEY"] = "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"

KECAMATAN_LIST = ["semua kecamatan", "Puger", "Kencong", "Sumbersari"]
DESA_LIST = ["semua desa", "Grenden", "puger kulon", "puger wetan"]
PRODUK_LIST = ["semua product", "Indihome", "Biznet", "By.u"]


kecamatan, desa = location_selector(KECAMATAN_LIST, DESA_LIST)
produk = product_selector(PRODUK_LIST)

qa_model = load_model()

if kecamatan and desa and produk:
    query = build_question(kecamatan, desa, produk)
    result = handle_question(qa_model, query)
    display_answer(result)