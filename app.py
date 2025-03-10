import streamlit as st
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.title("Monitoring Pemberitaan")
st.write("🚀 Selamat datang di dashboard monitoring pemberitaan!")

# ✅ Inisialisasi stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ✅ Daftar stopwords bahasa Indonesia yang diperluas
STOPWORDS = set([
    "yang", "dan", "di", "dengan", "ke", "dalam", "untuk", "atau", "kami","bagai","hingga","yakin","sendiri","mungkin","dukung","hanya","tempat",
    "kita", "ini", "itu", "pada", "adalah", "dari", "sebagai", "akan", "juga","pasti", "harap","sendiri","dukung","masuk", "jelas","upaya","tetapi",
    "telah", "agar", "maupun", "bagi", "tersebut", "dapat", "bahwa", "demi","butuh","langkah","sangat","penting","lanjut",
    "guna", "melalui", "sehingga", "lebih", "terhadap", "serta", "oleh", "perlu"
])

def bersihkan_teks(teks):
    """ Membersihkan teks dari karakter khusus & angka """
    teks = teks.lower()
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    return teks

def ekstrak_kata_kunci(teks, min_panjang=5, min_frekuensi=2):
    """ Ekstraksi kata kunci dengan filter stopwords, stemming, dan panjang kata """
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
    return kata_counter

def ekstrak_kutipan(teks):
    """ ✅ Perbaiki regex agar kutipan tidak kepotong dan ambil atribusi narasumber """
    kutipan_matches = re.findall(r'([“"])(.*?)([”"])(?:\s*(?:ujar|tambah|jelas|kata)\s*([A-Za-z\s]+))?', teks)
    kutipan_final = []
    
    for match in kutipan_matches:
        kutipan_teks = match[1]
        narasumber = match[3] if match[3] else "Tidak Diketahui"
        kutipan_final.append({"kutipan": kutipan_teks, "narasumber": narasumber})
    
    return kutipan_final

# ✅ Input dari user
st.subheader("📝 Input Siaran Pers")
input_teks = st.text_area("Masukkan teks siaran pers di sini:")

if st.button("Ekstrak Kata Kunci & Kutipan"):
    if input_teks:
        kata_kunci = ekstrak_kata_kunci(input_teks)
        kutipan = ekstrak_kutipan(input_teks)
        
        # ✅ Word Cloud untuk Kata Kunci
        st.subheader("🔑 Word Cloud Kata Kunci")
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white',
            colormap='coolwarm',
            contour_width=2, contour_color='steelblue',
            relative_scaling=0.5
        ).generate_from_frequencies(kata_kunci)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # ✅ Kutipan dalam format pointer
        st.subheader("💬 Kutipan yang Ditemukan")
        for item in kutipan:
            st.markdown(f"**{item['narasumber']}**")
            st.write(f"• {item['kutipan']}")
        
    else:
        st.warning("Masukkan teks terlebih dahulu!")

# ✅ Tambahkan atribusi
st.markdown("---")
st.markdown("**🔍 Ditenagai oleh:** [Sastrawi](https://github.com/har07/PySastrawi) & WordCloud")
