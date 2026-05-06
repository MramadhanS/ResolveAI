import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Import Middleware
from pydantic import BaseModel
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
import time 
from cachetools import TTLCache

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
chat_cache = TTLCache(maxsize=100, ttl=3600)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if query_engine is None:
        raise HTTPException(status_code=500, detail="Mesin RAG belum siap.")
    
    # 1. Cek apakah jawaban sudah ada di Cache
    user_query = request.pesan.strip().lower()
    if user_query in chat_cache:
        print(f"♻️ Cache Hit: Mengambil jawaban untuk '{user_query}' dari memori.")
        return ChatResponse(jawaban=chat_cache[user_query])

    # 2. Jika tidak ada di cache, jalankan logika Exponential Backoff
    max_retries = 3
    retry_delay = 3

    for attempt in range(max_retries):
        try:
            print(f"📡 Memanggil API Gemini untuk: {user_query}")
            response = query_engine.query(request.pesan)
            jawaban_final = str(response)

            # 3. Simpan jawaban ke Cache sebelum dikirim ke user
            chat_cache[user_query] = jawaban_final
            
            return ChatResponse(jawaban=jawaban_final)
            
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"⚠️ Limit tercapai. Retry {attempt+1} dlm {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise HTTPException(status_code=429, detail="Kuota penuh. Coba lagi nanti.")
            else:
                raise HTTPException(status_code=500, detail=str(e))