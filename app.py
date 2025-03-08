import streamlit as st
import re
import spacy
import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.title("Monitoring Pemberitaan")
st.write("🚀 Selamat datang di dashboard monitoring pemberitaan!")

# ✅ Cek & install SpaCy model jika belum ada
MODEL_PATH = "id_core_news_sm"
if not os.path.exists(spacy.util.get_model_path(MODEL_PATH)):
    os.system(f"python -m spacy download {MODEL_PATH}")

# ✅ Load model SpaCy IndoNLP
try:
    nlp = spacy.load(MODEL_PATH)
    spacy_status = "✅ Model SpaCy IndoNLP berhasil dimuat!"
except OSError:
    nlp = None
    spacy_status = "❌ Model SpaCy tidak ditemukan!"

# ✅ Inisialisasi stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def bersihkan_teks(teks):
    """ Membersihkan teks dari karakter khusus & angka """
    teks = teks.lower()
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    return teks

def ekstrak_kata_kunci(teks):
    """ Ekstraksi kata kunci menggunakan tokenisasi SpaCy + stemming Sastrawi """
    if nlp is None:
        return ["[ERROR] Model spaCy belum terinstal"]
    
    teks_bersih = bersihkan_teks(teks)
    doc = nlp(teks_bersih)
    
    kata_kunci = set()
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        kata_stem = stemmer.stem(token.text)
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

st.info(spacy_status)
