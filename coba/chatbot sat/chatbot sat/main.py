import os
from controller.chatbot_controller import load_model, handle_question, build_question
from view.chatbot_view import display_answer,  location_selector

# ===== Set API Key =====
os.environ["OPENAI_API_KEY"] = "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"

KECAMATAN_LIST = ["semua kecamatan", "Puger", "Kencong", "Sumbersari"]
DESA_LIST = ["semua desa", "Grenden", "puger kulon", "puger wetan"]

# ===== Streamlit App =====
# render_header()

kecamatan, desa = location_selector(KECAMATAN_LIST, DESA_LIST)

qa_model = load_model()
# question = input_user_query()

# result = handle_question(qa_model, question)

# if result:
#     display_answer(result)
#     # Uncomment if you want to see the source docs
#     # display_sources(result)

if kecamatan and desa:
    query = build_question(kecamatan, desa)
    result = handle_question(qa_model, query)
    display_answer(result)