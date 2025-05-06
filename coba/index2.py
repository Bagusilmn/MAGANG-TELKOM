import os
import streamlit as st
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ===== SET API KEY OPENROUTER =====
# os.environ["OPENAI_API_KEY"] = "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"

# ===== STREAMLIT UI =====
st.set_page_config(page_title="ChatBot Produk Telkomsel", layout="centered")
st.title("🤖 ChatBot Produk Telkomsel (RAG)")
st.caption("Powered by OpenRouter + LangChain + HuggingFace Embeddings")

query = st.text_input("Tanyakan apa pun tentang IndiHome, Orbit, Telkomsel One, dll:")

# ===== RAG SETUP =====
@st.cache_resource
def load_rag():
    loader = UnstructuredWordDocumentLoader("Data Product Telkomsel.docx")
    documents = loader.load()

    # Split dokumen
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    chunks = splitter.split_documents(documents)

    # Vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    # LLM OpenRouter
    llm = ChatOpenAI(
        model_name="hermes-3-llama-3.2-3b",
        # openai_api_key=os.environ["OPENAI_API_KEY"],
        openai_api_base="http://127.0.0.1:1234"
    )

    # Prompt khusus RAG
    prompt_template = """Anda adalah asisten digital Telkomsel.
Jawablah pertanyaan pengguna **hanya** berdasarkan informasi berikut:

{context}

Pertanyaan: {question}
Jawaban akurat dan lengkap berdasarkan data di atas:"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    # RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 100}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain

# Load pipeline
qa = load_rag()

# Handle pertanyaan
if query:
    with st.spinner("Sedang mencari jawaban..."):
        result = qa(query)

        # Output jawaban
        st.markdown("### 🧠 Jawaban:")
        st.markdown(result["result"])

        # # Debug: tampilkan isi chunk terambil
        # st.markdown("---")
        # st.markdown("#### 📄 Dokumen yang dijadikan referensi:")
        # for i, doc in enumerate(result["source_documents"]):
        #     st.markdown(f"**Dokumen {i+1}:**")
        #     st.text(doc.page_content[:100] + "...")
