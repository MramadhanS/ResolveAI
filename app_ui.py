import streamlit as st
import requests
import time

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="ResolveAI | MyPertamina Assistant",
    page_icon="⛽",
    layout="wide",
)

# 2. Definisi Warna (Deep Dark)
bg_main = "#101214"
bg_secondary = "#202327"
border_color = "#2F3336"
accent_blue = "#00529C" 
accent_red = "#E30613"  
accent_green = "#009E49" 

# 3. CSS Kustom - Fokus pada Stabilitas & Estetika Ikon
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .stApp {{
        background-color: {bg_main} !important;
        font-family: 'Inter', sans-serif;
    }}

    /* Header Profile */
    .header-wrapper {{
        position: fixed;
        top: 0; left: 0; right: 0; height: 70px;
        background-color: rgba(16, 18, 20, 0.98);
        border-bottom: 1px solid {border_color};
        display: flex; align-items: center; padding: 0 24px;
        z-index: 1000; backdrop-filter: blur(10px);
    }}

    .profile-pic {{
        width: 44px; height: 44px;
        background: linear-gradient(135deg, {accent_blue}, {accent_red}, {accent_green});
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 600; margin-right: 14px;
    }}

    /* Chat Container Tweaks */
    [data-testid="stChatMessage"] {{
        background-color: transparent !important;
        max-width: 800px; margin: 0 auto;
    }}

    /* Bubble Styling with Depth */
    [data-testid="stChatMessageUser"] > div {{
        background: linear-gradient(135deg, {accent_blue}, #003D75) !important;
        border-radius: 22px 22px 4px 22px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        color: white !important;
    }}

    [data-testid="stChatMessageAssistant"] > div {{
        background: linear-gradient(135deg, #2D3136, #202327) !important;
        border-radius: 22px 22px 22px 4px !important;
        border: 1px solid {border_color} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        color: white !important;
    }}

    /* Text Color Force */
    [data-testid="stChatMessage"] p {{
        color: white !important;
    }}

    /* Input Bar Style */
    .stChatInput {{
        max-width: 800px; margin: 0 auto; padding-bottom: 2rem;
    }}

    header, footer {{visibility: hidden;}}
</style>

<div class="header-wrapper">
    <div class="profile-pic">R</div>
    <div style="flex-grow: 1;">
        <b style="color:white; font-size:1.05rem; display:block;">ResolveAI</b>
        <span style="color:{accent_green}; font-size:0.75rem; font-weight:600;">● Online</span>
    </div>
</div>
<div style="margin-top: 90px;"></div>
""", unsafe_allow_html=True)

# 4. State Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo, Rama! Saya ResolveAI. Ada yang bisa saya bantu terkait MyPertamina?"}
    ]

# 5. Loop Chat dengan Ikon Sederhana (Menggunakan Parameter Avatar)
for message in st.session_state.messages:
    # Menggunakan avatar bawaan streamlit agar lebih stabil namun tetap ikonik
    avatar_icon = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 6. Logic Chat
if prompt := st.chat_input("Tulis pesan Anda..."):
    # Tampilkan Pesan User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("🔍 *Mencari solusi...*")
        
        try:
            # Pastikan URL FastAPI Benar
            response = requests.post(
                "http://127.0.0.1:8000/api/chat",
                json={"pesan": prompt},
                timeout=60
            )
            
            if response.status_code == 200:
                answer = response.json()["jawaban"]
                # Typing Effect
                displayed = ""
                for char in answer:
                    displayed += char
                    placeholder.markdown(displayed + "▊")
                    time.sleep(0.005)
                placeholder.markdown(displayed)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                placeholder.error("Backend bermasalah. Coba lagi.")
        except Exception as e:
            placeholder.error(f"Koneksi Gagal: {e}")