import streamlit as st
import google.generativeai as genai
import os
from pypdf import PdfReader

# 1. Tetapan Halaman
st.set_page_config(page_title="Sistem Aduan AI", layout="wide")
st.title("📋 Sistem Pemantauan & Penilaian Aduan")
st.write("Sistem pembantu harian untuk menilai aduan berdasarkan buku undang-undang.")

# 2. Kotak Sidebar (API Key & PDF)
with st.sidebar:
    st.header("Konfigurasi")
    api_key = st.text_input("Masukkan Gemini API Key anda:", type="password")
    st.markdown("---")
    st.write("### 📁 Langkah 1: Muat Naik Rujukan")
    buku_pdf = st.file_uploader("Muat naik Buku Undang-Undang (PDF)", type=["pdf"])

# 3. Lajur Input & Hasil AI
col1, col2 = st.columns(2)

with col1:
    st.write("### 📝 Kemasukan Aduan Baru")
    aduan = st.text_area("Tampal aduan di sini:", height=200)
    hantar = st.button("🚀 NILAI ADUAN SEKARANG")

with col2:
    st.write("### 🔍 Hasil Penilaian AI")
    if hantar:
        if not api_key:
            st.error("Sila masukkan API Key di sidebar sebelah kiri!")
        elif not buku_pdf:
            st.warning("Sila muat naik fail PDF rujukan terlebih dahulu!")
        elif not aduan:
            st.warning("Sila masukkan teks aduan!")
        else:
            with st.spinner("AI sedang membaca dokumen & menilai aduan..."):
                try:
                    # Konfigurasi API
                    genai.configure(api_key=api_key)
                    
                    # Baca fail PDF
                    reader = PdfReader(buku_pdf)
                    konteks = ""
                    for page in reader.pages:
                        t = page.extract_text()
                        if t: 
                            konteks += t
                    
                    # Arahan untuk AI
                    prompt = f"Rujukan Undang-Undang:\n{konteks[:40000]}\n\nAduan:\n{aduan}\n\nSila berikan penilaian dalam Bahasa Melayu."
                    
                    # --- SISTEM ANTI-RALAT AUTOMATIK ---
                    # Cuba guna model flash biasa dulu
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        respon = model.generate_content(prompt)
                    except Exception:
                        # Jika sangkut ralat v1beta, dia automatik tukar ke model backup ini
                        try:
                            model = genai.GenerativeModel('gemini-1.5-flash-latest')
                            respon = model.generate_content(prompt)
                        except Exception:
                            # Pilihan terakhir jika pelayan terlalu lama (legacy)
                            model = genai.GenerativeModel('gemini-pro')
                            respon = model.generate_content(prompt)
                    
                    st.success("Penilaian Selesai!")
                    st.write(respon.text)
                    
                except Exception as e:
                    st.error(f"Berlaku ralat sistem: {e}")
