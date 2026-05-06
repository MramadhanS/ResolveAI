# 🛡️ ResolveAI: Sentiment-Driven RAG Assistant
**Integrated Sentiment Analysis & Intelligent FAQ for MyPertamina Ecosystem.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-blue?style=flat)](https://www.llamaindex.ai/)

## 📌 Project Overview
**ResolveAI** adalah solusi chatbot berbasis AI yang mengintegrasikan **Analisis Sentimen** ulasan pengguna dengan teknologi **Retrieval-Augmented Generation (RAG)**. Proyek ini difokuskan untuk membantu pengguna ekosistem MyPertamina (Subsidi Tepat & LPG 3Kg) dalam menemukan solusi teknis secara instan melalui percakapan alami.

### 🎯 The Problem
Berdasarkan analisis pada ribuan ulasan di Google Play Store, ditemukan pola di mana pengguna cenderung langsung memberikan **rating 1** saat menghadapi kendala teknis, meskipun solusi sebenarnya sudah tersedia di halaman FAQ resmi. Hal ini terjadi karena pengguna merasa kesulitan atau enggan mengeksplorasi dokumen FAQ statis yang panjang.

### 💡 The Solution
ResolveAI hadir sebagai jembatan informasi. Alih-alih mencari satu per satu di FAQ, pengguna dapat langsung menanyakan kendala mereka kepada chatbot. AI akan secara cerdas mengambil konteks dari dokumen SOP resmi dan memberikan jawaban yang relevan dan solutif secara instan.

---

## 🛠️ Tech Stack & Architecture
*   **Core Engine:** **LlamaIndex** untuk manajemen Vector Database & Retrieval.
*   **LLM:** **Google Gemini 1.5 Flash** (via Google AI Studio).
*   **Sentiment Research:** Python (Pandas, Matplotlib) untuk mapping masalah utama pengguna dari dataset ulasan.
*   **Backend:** **FastAPI** dengan fitur *Exponential Backoff* & *TTLCache*.
*   **Frontend:** **Streamlit** dengan kustomisasi Messenger-style Dark UI.

---

## 🚀 Key Features
*   **Direct-to-Solution:** Memangkas waktu pencarian solusi di FAQ konvensional menjadi satu baris pertanyaan.
*   **Ecosystem Wide:** Mencakup panduan Subsidi Tepat kendaraan roda 4 hingga pendaftaran subsidi LPG 3Kg.
*   **Resilient API Handling:** Menggunakan teknik *retry* otomatis untuk menjaga kestabilan layanan pada tier API gratis.
*   **Modern Interaction:** Antarmuka chat yang intuitif, ringan, dan responsif.

---

## 📈 Engineering Highlights (Evaluation)
*   **Accuracy:** Berhasil memberikan jawaban akurat untuk **10+ skenario kritis** (Verifikasi STNK, Kendala OTP, Banding Nopol, hingga Registrasi LPG).
*   **Performance:** Rata-rata waktu respon **~5 detik** (sudah termasuk mekanisme *automated retry* untuk memastikan keandalan jawaban).
*   **Context Adherence:** Sistem dikunci hanya untuk menjawab berdasarkan dokumen *knowledge base* MyPertamina guna menghindari halusinasi data.

---

## 📁 Project Structure
```text
.
├── data/
│   └── knowledge_base/   # Koleksi SOP MyPertamina & LPG (Markdown)
├── notebooks/            # Analisis sentimen ulasan Play Store
├── main.py               # Backend FastAPI & RAG Logic
├── app.py                # Frontend Streamlit (Messenger UI)
├── requirements.txt      # Library dependencies
