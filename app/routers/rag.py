# app/routers/rag.py

import os
from fastapi import APIRouter, Depends
from dotenv import load_dotenv

# Impor komponen-komponen LangChain & model Pydantic kita
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from ..models.rag_models import QueryRequest, QueryResponse

from fastapi.responses import StreamingResponse
import asyncio

# Impor baru untuk memory
# from langchain.memory import ConversationBufferMemory
# from langchain_redis import RedisChatMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
# from langchain.chains import ConversationalRetrievalChain

from langchain_openai import ChatOpenAI
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_classic.chains import create_retrieval_chain
from langchain_classic import hub

# --- Setup Awal ---
# Kita pindahkan logika setup ke sini.
# Dalam aplikasi produksi, ini sering dilakukan di tempat lain (misal, startup event).

# Muat environment variable
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Tambahkan pemeriksaan yang kuat di awal
if not google_api_key:
    raise ValueError("FATAL ERROR: GOOGLE_API_KEY environment variable is not set.")

# Inisialisasi komponen-komponen yang mahal hanya sekali
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key, temperature=0)
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embedding_function,
    collection_name="indonesian_tech"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Definisikan template prompt
prompt_template_str = """
Anda adalah asisten AI yang cerdas. Gunakan HANYA 'KONTEKS' yang diberikan untuk menjawab 'PERTANYAAN'.
Jika jawaban tidak ada dalam konteks, jawab: 'Maaf, saya tidak dapat menemukan informasi mengenai hal tersebut di dalam data saya.'

KONTEKS:
{context}

PERTANYAAN:
{input}

JAWABAN:
"""
prompt_template = ChatPromptTemplate.from_template(prompt_template_str)

# Bangun rantai RAG
rag_chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)
print("✅ Rantai RAG siap digunakan oleh API.")

# Kita akan membuat rantai yang sedikit berbeda untuk percakapan.
# ConversationalRetrievalChain adalah cara yang mudah untuk ini.
# Perhatikan bahwa kita tidak membuat objek memori di sini.
combine_docs_chain = create_stuff_documents_chain(
    llm, prompt_template
)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
print("✅ Rantai RAG Percakapan siap digunakan.")

# --- Router API ---
router = APIRouter()

@router.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest) -> QueryResponse:
    """
    Menerima pertanyaan, memprosesnya melalui rantai RAG,
    dan mengembalikan jawabannya.
    """
    # Panggil rantai LangChain dengan pertanyaan dari request
    answer_text = rag_chain.invoke(request.question)
    
    # Kembalikan jawaban dalam format Pydantic model QueryResponse
    return QueryResponse(answer=answer_text)

# --- ENDPOINT BARU DENGAN MEMORY ---
@router.post("/chat", response_model=QueryResponse)
def chat_with_rag(request: QueryRequest, session_id: str = "default_session"):
    """
    Endpoint chat yang memiliki memori, disimpan di Redis.
    Gunakan 'session_id' yang berbeda untuk percakapan yang berbeda.
    """
    # Buat objek histori yang terhubung ke Redis untuk sesi ini.
    # Host-nya adalah 'redis', nama layanan kita di docker-compose.yml!
    message_history = RedisChatMessageHistory(
        url="redis://redis:6379/0", session_id=session_id
    )

    # Panggil rantai percakapan
    result = retrieval_chain.invoke({
        "input": request.question,
        "chat_history": message_history.messages,
    })

    # Dapatkan jawaban
    answer = result["answer"]

    # Simpan interaksi baru ini ke Redis secara manual
    message_history.add_user_message(request.question)
    message_history.add_ai_message(answer)
    
    return QueryResponse(answer=answer)