import streamlit as st
import requests
import json

# Tetapan paparan penuh
st.set_page_config(page_title="Sistem Penilaian Aduan", layout="wide")

# 1. SIDEBAR KIRI (KONFIGURASI)
st.sidebar.title("Konfigurasi")
api_key = st.sidebar.text_input("Masukkan Gemini API Key anda:", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📁 Langkah 1: Muat Naik Rujukan")
uploaded_file = st.sidebar.file_uploader("Muat naik Buku Undang-Undang (PDF)", type=["pdf"])
if uploaded_file:
    st.sidebar.caption("200MB per file • PDF")

# 2. KAWASAN UTAMA (KANAN)
st.title("📋 Sistem Pemantauan & Penilaian Aduan")
st.write("Sistem pembantu harian untuk menilai aduan berdasarkan buku undang-undang.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Kemasukan Aduan Baru")
    aduan_text = st.text_area("Tampal aduan di sini:", height=300, placeholder="Taip atau tampal kes aduan di sini...")
    btn_nilai = st.button("🚀 NILAI ADUAN SEKARANG")

with col2:
    st.markdown("### 🔍 Hasil Penilaian AI")
    
    if btn_nilai:
        if not api_key:
            st.error("Sila masukkan API Key di sidebar kiri terlebih dahulu!")
        elif not aduan_text:
            st.error("Sila masukkan teks aduan!")
        else:
            with st.spinner("AI sedang menilai aduan, sila tunggu..."):
                # Menggunakan jalan raya v1 yang stabil agar tidak keluar ralat 404
               url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
                headers = {"Content-Type": "application/json"}
                prompt_penuh = f"Anda adalah pakar undang-undang. Sila nilaikan aduan berikut secara rasmi dan jelas dalam Bahasa Melayu serta berikan cadangan tindakan:\n\n{aduan_text}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt_penuh}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        output_text = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.markdown(output_text)
                    else:
                        st.error(f"Ralat API ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Ralat Sistem: {str(e)}")
