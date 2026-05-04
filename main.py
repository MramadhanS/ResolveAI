import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# 1. Persiapan Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

Settings.llm = Gemini(model="models/gemini-2.5-flash", api_key=api_key)
Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-2", api_key=api_key)

# Variabel global untuk menyimpan memori AI
query_engine = None

# 2. Siklus Hidup Aplikasi (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global query_engine
    print("Membangun Vector Database dari SOP Pertamina...")
    try:
        # Membaca dokumen dari folder knowledge_base
        documents = SimpleDirectoryReader("data/knowledge_base/").load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        print("Sistem RAG Berhasil Aktif dan Siap Menerima Pesan!")
    except Exception as e:
        print(f"Gagal membangun index: {e}")
    yield
    print("Server dimatikan, memori dibersihkan.")

# 3. Inisialisasi Aplikasi FastAPI (INI YANG TADI HILANG/ERROR)
app = FastAPI(
    title="ResolveAI - Pertamina CS",
    description="Backend API RAG untuk Asisten Virtual Pertamina",
    version="1.0.0",
    lifespan=lifespan
)

# 4. Struktur Data Input & Output (Pydantic)
class ChatRequest(BaseModel):
    pesan: str

class ChatResponse(BaseModel):
    jawaban: str

# 5. Endpoint Utama untuk Chatting
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not query_engine:
        raise HTTPException(status_code=500, detail="Mesin RAG belum siap.")
    
    try:
        respon_ai = query_engine.query(request.pesan)
        return ChatResponse(jawaban=str(respon_ai))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))