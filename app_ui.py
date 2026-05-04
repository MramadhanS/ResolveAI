import streamlit as st
import requests

# 1. Konfigurasi Halaman - Vibes Profesional
st.set_page_config(
    page_title="ResolveAI | Solusi MyPertamina",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Injeksi CSS Kustom - Glassmorphism & Custom Branding
st.markdown("""
<style>
    /* Global Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Background untuk Header */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }

    /* Menyembunyikan elemen bawaan */
    header, footer, #MainMenu {visibility: hidden;}

    /* Styling Container Header */
    .header-container {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        margin-bottom: 2rem;
        border-top: 5px solid #1E3A8A; /* Border Biru Pertamina */
    }

    .main-header {
        font-size: 2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1rem;
        color: #64748B;
        line-height: 1.5;
    }

    /* Chat Message Styling */
    .stChatMessage {
        background-color: transparent !important;
        padding: 1rem 0;
    }

    /* Custom Avatar Box */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #EF4444 !important; /* Merah Pertamina untuk User */
    }
    
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #1E3A8A !important; /* Biru Pertamina untuk AI */
    }

    /* Input Bar Styling */
    .stChatInputContainer {
        padding-bottom: 2rem;
    }

    /* Info Badge */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        background-color: #E0F2FE;
        color: #0369A1;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Bagian Header UI - Menggunakan Container
st.markdown(f"""
<div class="header-container">
    <div class="main-header">🛡️ ResolveAI</div>
    <div class="sub-header">
        Asisten Digital Pendaftaran Subsidi Tepat MyPertamina.<br>
        Siap membantu kendala Foto STNK, KTP, dan Kode OTP Anda.
    </div>
    <div class="status-badge">Sistem Terintegrasi Knowledge Base 2026</div>
</div>
""", unsafe_allow_html=True)

# 4. Inisialisasi Memori Obrolan
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya **ResolveAI**. Jika Anda mengalami kendala saat upload STNK atau OTP belum masuk, silakan tanyakan di sini. Apa yang bisa saya bantu?"}
    ]

# 5. Quick Actions (Agar tidak flat, tambahkan tombol bantuan cepat)
st.write("---")
cols = st.columns(3)
with cols[0]:
    if st.button("📸 Masalah Foto STNK"):
        st.session_state.temp_prompt = "Kenapa foto STNK saya ditolak terus?"
with cols[1]:
    if st.button("📧 OTP Tidak Masuk"):
        st.session_state.temp_prompt = "Kode OTP saya tidak masuk ke email"
with cols[2]:
    if st.button("🚗 Nopol Terdaftar"):
        st.session_state.temp_prompt = "Beli mobil bekas tapi nopol sudah terdaftar"

# 6. Tampilkan Riwayat Obrolan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Logika Input
prompt = st.chat_input("Ketik kendala MyPertamina Anda...")

# Handle tombol quick action jika diklik
if "temp_prompt" in st.session_state:
    prompt = st.session_state.temp_prompt
    del st.session_state.temp_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Mencari solusi di database MyPertamina...*")
        
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/chat",
                json={"pesan": prompt},
                timeout=30 
            )
            
            if response.status_code == 200:
                jawaban_ai = response.json()["jawaban"]
                message_placeholder.markdown(jawaban_ai)
                st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})
            else:
                message_placeholder.error(f"Server sibuk (Error {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            message_placeholder.markdown("⚠️ **Backend Offline.** Jalankan `uvicorn main:app` di terminal.")
        except Exception as e:
            message_placeholder.markdown(f"⚠️ **Error:** {e}")