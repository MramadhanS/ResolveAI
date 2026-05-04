import streamlit as st
import requests

# 1. Konfigurasi Halaman (Harus diletakkan paling atas)
st.set_page_config(
    page_title="ResolveAI | Pertamina CS",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Injeksi CSS Kustom untuk Estetika Profesional dan Minimalis
st.markdown("""
<style>
    /* Menyembunyikan menu bawaan Streamlit agar terlihat seperti aplikasi mandiri */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Desain Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A; /* Biru Korporat */
        margin-bottom: 0rem;
        padding-bottom: 0rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Bagian Header UI
st.markdown('<div class="main-header">ResolveAI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Pusat Bantuan & Informasi Layanan LPG 3 Kg</div>', unsafe_allow_html=True)
st.divider()

# 4. Inisialisasi Memori Obrolan (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya adalah ResolveAI, asisten virtual Anda. Ada yang bisa saya bantu terkait regulasi atau layanan pangkalan LPG 3 Kg hari ini?"}
    ]

# 5. Tampilkan Riwayat Obrolan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Menangani Input Pengguna
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Tampilkan pesan pengguna di layar
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Siapkan animasi loading saat AI berpikir
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*(Mengetik jawaban...)*")
        
        try:
            # Mengirim pertanyaan ke Backend FastAPI kita
            response = requests.post(
                "http://127.0.0.1:8000/api/chat",
                json={"pesan": prompt},
                timeout=30 # Batas waktu tunggu 30 detik
            )
            
            if response.status_code == 200:
                # Ambil jawaban JSON dari Backend
                jawaban_ai = response.json()["jawaban"]
                message_placeholder.markdown(jawaban_ai)
                # Simpan jawaban ke memori
                st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})
            else:
                st.error(f"Error dari server: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            message_placeholder.markdown("⚠️ **Koneksi Terputus.** Pastikan server FastAPI (main.py) sedang menyala di terminal lain.")
        except Exception as e:
            message_placeholder.markdown(f"⚠️ **Terjadi Kesalahan:** {e}")