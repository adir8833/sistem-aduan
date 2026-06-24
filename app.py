import streamlit as str
import google.generativeai as genai
from pypdf import PdfReader

# REKABENTUK ANTARAMUKA (INTERFACE)
str.set_page_config(page_title="Sistem Penilaian Aduan AI", layout="wide")
str.title("📋 Sistem Pemantauan & Penilaian Aduan")
str.write("Sistem pembantu harian untuk menilai aduan berdasarkan buku undang-undang.")

# MASUKKAN KUNCI API
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Masukkan Gemini API Key anda:", type="password")

str.sidebar.markdown("---")
str.sidebar.write("### 📁 Langkah 1: Muat Naik Rujukan")
buku_pdf = str.sidebar.file_uploader("Muat naik Buku Undang-Undang (PDF)", type=["pdf"])

# BAHAGIAN UTAMA SISTEM
kolum_kiri, kolum_kanan = str.columns(2)

with kolum_kiri:
    str.subheader("📝 Kemasukan Aduan Baru")
    teks_aduan = str.text_area("Tampal (Paste) teks aduan di sini:", height=250)
    butang_nilai = str.button("🚀 NILAI ADUAN SEKARANG")

with kolum_kanan:
    str.subheader("🔍 Hasil Penilaian AI")
    
    if butang_nilai:
        if not api_key:
            str.error("Sila masukkan API Key anda di bahagian tepi kiri dahulu!")
        elif not buku_pdf:
            str.error("Sila muat naik fail PDF undang-undang rujukan anda dahulu!")
        elif not teks_aduan:
            str.error("Sila masukkan teks aduan untuk dinilai!")
        else:
            with str.spinner("AI sedang membaca undang-undang dan menilai aduan... Sila tunggu."):
                try:
                    # 1. Baca fail PDF undang-undang
                    pembaca_pdf = PdfReader(buku_pdf)
                    teks_undang_undang = ""
                    # Ambil 50 muka surat pertama dahulu supaya proses laju & tak hantar data terlalu besar
                    for i in range(min(50, len(pembaca_pdf.pages))):
                        teks_undang_undang += pembaca_pdf.pages[i].extract_text()
                    
                    # 2. Set up AI
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # 3. Arahan kepada AI (Prompt)
                    arahan = f"""
                    Anda adalah seorang pakar undang-undang dan pegawai penilai aduan yang sangat teliti.
                    Tugasan anda adalah membantu pengguna menilai aduan berdasarkan teks undang-undang yang disediakan di bawah.
                    
                    RUJUKAN UNDANG-UNDANG:
                    {teks_undang_undang[:30000]} 
                    
                    ADUAN PENGGUNA:
                    {teks_aduan}
                    
                    Sila berikan penilaian anda dalam format berikut (gunakan tulisan tebal/bold untuk tajuk):
                    1. **Cadangan Akta & Seksyen yang Berkaitan**: Sebutkan nama akta dan seksyen spesifik yang menyentuh kesalahan dalam aduan ini berdasarkan rujukan yang diberi.
                    2. **Justifikasi / Ulasan Penilaian**: Terangkan secara ringkas mengapa seksyen ini dipilih berdasarkan fakta aduan.
                    3. **Syor Tindakan**: Apakah maklumat tambahan atau semakan yang perlu dilakukan oleh pegawai untuk mengesahkan aduan ini.
                    
                    Jawab dalam Bahasa Melayu yang profesional dan mudah difahami. Jangan reka maklumat jika tiada dalam rujukan.
                    """
                    
                    # 4. Jana jawapan
                    respons = model.generate_content(arahan)
                    str.success("Penilaian Selesai!")
                    str.markdown(respons.text)
                    
                except Exception as e:
                    str.error(f"Berlaku ralat: {str(e)}")
                    
