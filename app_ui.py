import streamlit as st
import requests

# 1. Konfigurasi Halaman - Dark Theme Vibes
st.set_page_config(
    page_title="ResolveAI | Dark Mode",
    page_icon="🌑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Injeksi CSS Kustom - Dark Mode & Neon Accents
st.markdown("""
<style>
    /* Mengubah latar belakang seluruh aplikasi ke Dark */
    .stApp {
        background-color: #0F172A; /* Slate 900 */
        color: #F8FAFC;
    }

    /* Menyembunyikan elemen bawaan */
    header, footer, #MainMenu {visibility: hidden;}

    /* Styling Container Header - Glassmorphism Dark */
    .header-container {
        background: rgba(30, 41, 59, 0.7); /* Slate 800 with opacity */
        padding: 2.5rem;
        border-radius: 24px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 2.5rem;
    }

    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 400;
    }

    /* Chat Bubbles Styling */
    [data-testid="stChatMessage"] {
        background-color: #1E293B !important; /* Slate 800 */
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Menyesuaikan warna teks input chat */
    .stChatInput textarea {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
    }

    /* Badge Status */
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.1);
        color: #38BDF8;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-top: 1rem;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0F172A;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header UI
st.markdown("""
<div class="header-container">
    <div class="main-header">ResolveAI Assistant</div>
    <div class="sub-header">
        Sistem Pakar Resolusi Kendala MyPertamina.<br>
        Navigasi cerdas untuk pendaftaran dan verifikasi data Anda.
    </div>
    <div class="status-pill">● Neural Engine Active</div>
</div>
""", unsafe_allow_html=True)

# 4. Inisialisasi Memori Obrolan
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo, Rama. Ada kendala teknis apa dengan MyPertamina hari ini? Saya siap menganalisis solusi dari database terbaru."}
    ]

# 5. Tampilkan Riwayat Obrolan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Area Input Chat
if prompt := st.chat_input("Gambarkan kendala Anda secara detail..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon Assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⚡ *Menganalisis repositori pengetahuan...*")
        
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
                message_placeholder.error(f"Koneksi Server Gagal ({response.status_code})")
                
        except requests.exceptions.ConnectionError:
            message_placeholder.markdown("⚠️ **Terminal Error.** Pastikan backend FastAPI Anda aktif di port 8000.")
        except Exception as e:
            message_placeholder.markdown(f"⚠️ **System Failure:** {e}")