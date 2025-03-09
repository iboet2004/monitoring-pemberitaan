import streamlit as st
import re
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.title("Monitoring Pemberitaan")
st.write("🚀 Selamat datang di dashboard monitoring pemberitaan!")

# ✅ Inisialisasi stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ✅ Daftar stopwords bahasa Indonesia
STOPWORDS = set([
    "yang", "dan", "di", "dengan", "ke", "dalam", "untuk", "atau", "kami",
    "kita", "ini", "itu", "pada", "adalah", "dari", "sebagai", "akan", "juga",
    "telah", "agar", "maupun", "bagi", "tersebut", "dapat", "bahwa", "demi"
])

def bersihkan_teks(teks):
    """ Membersihkan teks dari karakter khusus & angka """
    teks = teks.lower()
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    return teks

def ekstrak_kata_kunci(teks, min_panjang=5, min_frekuensi=2):
    """ Ekstraksi kata kunci dengan filter stopwords dan panjang kata """
    teks_bersih = bersihkan_teks(teks)
    
    # ✅ Gunakan regex untuk tokenisasi
    tokens = re.split(r'\s+', teks_bersih)  

    kata_kunci = []
    for token in tokens:
        kata_stem = stemmer.stem(token)  # Stemming bahasa Indonesia
        if len(kata_stem) >= min_panjang and kata_stem not in STOPWORDS:
            kata_kunci.append(kata_stem)

    # ✅ Hitung frekuensi kata dan ambil yang muncul lebih dari min_frekuensi
    kata_counter = Counter(kata_kunci)
    kata_terpilih = [k for k, v in kata_counter.items() if v >= min_frekuensi]

    return kata_terpilih

def ekstrak_kutipan(teks):
    """ ✅ Perbaiki regex agar kutipan tidak kepotong """
    kutipan = re.findall(r'(["“][^"”]+["”])', teks)
    return [k.replace("“", '"').replace("”", '"') for k in kutipan]

# ✅ Input dari user
st.subheader("📝 Input Siaran Pers")
input_teks = st.text_area("Masukkan teks siaran pers di sini:")

if st.button("Ekstrak Kata Kunci & Kutipan"):
    if input_teks:
        kata_kunci = ekstrak_kata_kunci(input_teks)
        kutipan = ekstrak_kutipan(input_teks)
        
        st.subheader("🔑 Kata Kunci yang Ditemukan")
        st.write(", ".join(kata_kunci) if kata_kunci else "Tidak ada kata kunci ditemukan.")

        st.subheader("💬 Kutipan yang Ditemukan")
        st.write(kutipan if kutipan else "Tidak ada kutipan ditemukan.")
    else:
        st.warning("Masukkan teks terlebih dahulu!")
