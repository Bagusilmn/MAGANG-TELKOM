import os
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import streamlit as st

# Set API Key
# os.environ["OPENAI_API_KEY"] = "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"

@st.cache_resource
def load_chatbot():
    loader = UnstructuredWordDocumentLoader("D:\Magang telkom\coba\inicobaeco\chatbot.docx")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=500)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    llm = ChatOpenAI(
        model_name="deepseek/deepseek-r1:free",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1"
    )

    prompt_template = """Anda adalah asisten digital Telkomsel.
Jawablah pertanyaan pengguna **hanya** berdasarkan informasi berikut:

{context}

Pertanyaan: {question}
Jawaban akurat dan lengkap berdasarkan data di atas:"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 100}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain

def get_chatbot_response(qa, query):
    return qa(query)
