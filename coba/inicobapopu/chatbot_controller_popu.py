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
    loader = UnstructuredWordDocumentLoader("Data Product Telkomsel.docx")
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
