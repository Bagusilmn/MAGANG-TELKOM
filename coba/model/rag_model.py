import os
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def initialize_rag():
    loader = UnstructuredWordDocumentLoader("Data Product Telkomsel.docx")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=500)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    # Inisialisasi model
    llm = OpenAI(
        model_name="hermes-3-llama-3.2-3b",
        openai_api_key= "sk-fake-key",
        openai_api_base="http://127.0.0.1:1234/v1",
        temperature=0.7
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
