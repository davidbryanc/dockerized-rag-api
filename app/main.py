from fastapi import FastAPI
from .routers import rag # Impor modul rag.py dari paket routers

app = FastAPI(
    title="AI Engineer Learning API",
    description="API untuk menguji coba berbagai konsep AI, termasuk RAG."
)

# Sambungkan router RAG ke aplikasi utama
app.include_router(
    rag.router,
    prefix="/rag", # Semua endpoint di router ini akan diawali dengan /rag
    tags=["RAG Service"]
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang! Silakan kunjungi /docs untuk melihat endpoint yang tersedia."}
