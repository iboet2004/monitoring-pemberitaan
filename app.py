import streamlit as st
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

# Download stopwords
nltk.download("punkt")
nltk.download("stopwords")

# Inisialisasi stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Stopwords tambahan untuk filtering
custom_stopwords = set(stopwords.words("indonesian"))
custom_stopwords.update({"guna", "dalam", "akan", "dan", "untuk", "yang", "dengan", "ini", "itu", "pada"})

def extract_keywords(text):
    words = word_tokenize(text.lower())
    words = [stemmer.stem(word) for word in words if word.isalnum() and word not in custom_stopwords]
    return list(set(words))  # Hilangkan duplikasi

def extract_quotes(text):
    quotes = re.findall(r'\"(.*?)\"', text)
    return quotes

# UI Streamlit
st.title("🔎 Ekstraksi Kata Kunci & Kutipan")
uploaded_file = st.file_uploader("Upload Siaran Pers (.txt)", type=["txt"])

if uploaded_file is not None:
    raw_text = uploaded_file.read().decode("utf-8")
    keywords = extract_keywords(raw_text)
    quotes = extract_quotes(raw_text)
    
    st.subheader("🔑 Kata Kunci yang Ditemukan")
    st.write(", ".join(keywords))
    
    st.subheader("💬 Kutipan yang Ditemukan")
    for idx, quote in enumerate(quotes):
        st.write(f"{idx+1}. {quote}")
    
    # Atribusi
    st.markdown("**Ditenagai oleh:** [Sastrawi](https://github.com/har07/PySastrawi) & [NLTK](https://www.nltk.org/)")
