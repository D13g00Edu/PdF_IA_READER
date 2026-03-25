import json
import os
import shutil
from datetime import datetime

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)

from app.core.config import VECTORDB_DIR, METADATA_PATH, GOOGLE_API_KEY

vectorstore = None


def get_api_key():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY no está configurada. Define la variable de entorno GOOGLE_API_KEY.")
    return GOOGLE_API_KEY


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=get_api_key(),
    )

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()


def split_pdf(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return text_splitter.split_documents(documents)


def create_vectorstore(chunks):
    embeddings = get_embeddings()
    return FAISS.from_documents(chunks, embeddings)


def set_vectorstore(vs):
    global vectorstore
    vectorstore = vs


def get_vectorstore():
    return vectorstore


def search_similar_chunks(question: str, k: int = 1):
    if vectorstore is None:
        return None
    return vectorstore.similarity_search(question, k=k)

def answer_with_context(question: str, chunks):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=get_api_key(),
        temperature=0
    )

    context = "\n\n".join(
        [f"[Chunk {i+1}]\n{doc.page_content}" for i, doc in enumerate(chunks)]
    )

    prompt = f"""
                Eres un asistente que responde SOLO con la información del contexto.
                Hablas breve, natural y amable.
                Si la respuesta no está en el contexto, responde exactamente:
                "No encontré esa información en el PDF."
                Contexto:
                {context}
                Pregunta:
                {question}
                """

    response = llm.invoke(prompt)
    return response.content

def save_vectorstore():
    global vectorstore
    if vectorstore is None:
        return
    vectorstore.save_local(VECTORDB_DIR)


def load_vectorstore_from_disk():
    global vectorstore

    index_file = os.path.join(VECTORDB_DIR, "index.faiss")
    pkl_file = os.path.join(VECTORDB_DIR, "index.pkl")

    if not os.path.exists(index_file) or not os.path.exists(pkl_file):
        return None

    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        VECTORDB_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore


def save_metadata(data: dict):
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_metadata():
    if not os.path.exists(METADATA_PATH):
        return None

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_metadata(original_filename: str, stored_filename: str, pages: int, chunks: int):
    return {
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "pages": pages,
        "chunks": chunks,
        "uploaded_at": datetime.utcnow().isoformat()
    }


def clear_saved_index():
    if os.path.exists(VECTORDB_DIR):
        shutil.rmtree(VECTORDB_DIR)
    os.makedirs(VECTORDB_DIR, exist_ok=True)