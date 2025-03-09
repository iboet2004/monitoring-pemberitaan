import streamlit as st
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.title("Monitoring Pemberitaan")
st.write("🚀 Selamat datang di dashboard monitoring pemberitaan!")

# ✅ Inisialisasi stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def bersihkan_teks(teks):
    """ Membersihkan teks dari karakter khusus & angka """
    teks = teks.lower()
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    return teks

def ekstrak_kata_kunci(teks):
    """ Ekstraksi kata kunci menggunakan regex tokenization + stemming Sastrawi """
    teks_bersih = bersihkan_teks(teks)
    
    # ✅ Gunakan regex untuk tokenisasi, bukan NLTK
    tokens = re.split(r'\s+', teks_bersih)  # Pecah teks berdasarkan spasi
    
    kata_kunci = set()
    for token in tokens:
        kata_stem = stemmer.stem(token)  # Stemming bahasa Indonesia
        if len(kata_stem) > 3:  # Filter kata pendek biar lebih relevan
            kata_kunci.add(kata_stem)

    return list(kata_kunci)

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
