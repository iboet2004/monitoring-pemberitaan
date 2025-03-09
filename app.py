import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Pastikan stopwords tersedia
nltk.download('stopwords')
id_stopwords = set(stopwords.words('indonesian'))

# Inisialisasi Stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())  # Ambil kata minimal 3 huruf
    filtered_words = [word for word in words if word not in id_stopwords]  # Hapus stopwords
    stemmed_words = [stemmer.stem(word) for word in filtered_words]  # Stemming
    unique_keywords = list(set(stemmed_words))  # Hilangkan duplikasi
    return unique_keywords

def extract_quotes(text):
    quotes = re.findall(r'\"(.*?)\"', text)  # Ambil teks dalam tanda kutip
    return quotes

# Load siaran pers dari user
st.title("🔎 Ekstraksi Kata Kunci & Kutipan")
uploaded_file = st.file_uploader("Upload Siaran Pers (TXT)", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    
    # Ekstraksi kata kunci dan kutipan
    keywords = extract_keywords(text)
    quotes = extract_quotes(text)
    
    # Tampilkan hasil
    st.markdown("### 🟡 Kata Kunci yang Ditemukan")
    st.write(", ".join(keywords))
    
    st.markdown("### 💬 Kutipan yang Ditemukan")
    for idx, quote in enumerate(quotes):
        st.write(f"{idx+1}. {quote}")
    
    # Atribusi
    st.markdown("---")
    st.markdown("**🔍 Sumber:** Algoritma NLP dengan NLTK & Sastrawi")
