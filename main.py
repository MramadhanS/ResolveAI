import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Import Middleware
from pydantic import BaseModel
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# 1. Persiapan Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Menggunakan model Gemini 3 Flash sesuai kapabilitas sistem terbaru
Settings.llm = Gemini(model="models/gemini-2.5-flash", api_key=api_key)
Settings.embed_model = GeminiEmbedding(model_name="models/gemini-embedding-2", api_key=api_key)

# Variabel global untuk query engine
query_engine = None

# 2. Siklus Hidup Aplikasi (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global query_engine
    print("Membangun Vector Database dari SOP Pertamina...")
    try:
        # Pastikan path folder benar
        if not os.path.exists("data/knowledge_base/"):
            raise Exception("Folder 'data/knowledge_base/' tidak ditemukan!")
            
        documents = SimpleDirectoryReader("data/knowledge_base/").load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine(streaming=False)
        print("Sistem RAG Berhasil Aktif!")
    except Exception as e:
        print(f"Gagal membangun index: {e}")
    yield
    print("Server dimatikan.")

# 3. Inisialisasi FastAPI
app = FastAPI(
    title="ResolveAI - Backend",
    lifespan=lifespan
)

# --- TAMBAHKAN CORS MIDDLEWARE DI SINI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua origin termasuk Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Schema Data
class ChatRequest(BaseModel):
    pesan: str

class ChatResponse(BaseModel):
    jawaban: str

# 5. Endpoint Chat
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if query_engine is None:
        raise HTTPException(status_code=500, detail="Mesin RAG belum siap.")
    
    try:
        # Menjalankan query ke LlamaIndex
        response = query_engine.query(request.pesan)
        return ChatResponse(jawaban=str(response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error AI: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)