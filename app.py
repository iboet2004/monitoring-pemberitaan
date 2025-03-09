import re
import string
import nltk
from nltk.corpus import stopwords
from collections import Counter
import streamlit as st

# Pastikan stopwords telah diunduh
nltk.download("stopwords")

# Fungsi untuk ekstraksi kata kunci yang lebih tajam
def extract_keywords(text, top_n=20):
    stop_words = set(stopwords.words("indonesian"))
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())  # Ambil hanya kata
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    word_counts = Counter(filtered_words)
    return [word for word, _ in word_counts.most_common(top_n)]

# Fungsi untuk ekstraksi kutipan secara lebih akurat
def extract_quotes(text):
    quotes = re.findall(r'\"(.*?)\"', text)
    return quotes

# Contoh input siaran pers
siaran_pers = """
Badan Informasi Geospasial (BIG) dan Kementerian Komunikasi dan Digital (Komdigi) bekerja sama dalam pengembangan Peta Digital Nasional guna memperkuat kedaulatan digital Indonesia. Peta ini akan menjadi dasar dalam perencanaan dan pengambilan kebijakan berbasis data, serta mendukung berbagai sektor, termasuk tata ruang, infrastruktur, dan lingkungan.

Peta Digital Nasional akan memberikan informasi geospasial yang akurat dan terstandarisasi, memungkinkan perencanaan pembangunan yang lebih efektif, termasuk dalam optimalisasi jaringan serat optik dan pemetaan lokasi Base Transceiver Station (BTS) untuk konektivitas digital.

Menteri Komunikasi dan Digital, Meutya Hafid, menekankan bahwa pengembangan Peta Digital Nasional sejalan dengan upaya pemerintah dalam mewujudkan kedaulatan digital. "Kami menempatkan kedaulatan digital sebagai prioritas dalam transformasi digital nasional. Jika kita dapat menggunakan peta digital yang kita kembangkan sendiri, ini merupakan langkah besar dalam memperkuat ketahanan digital Indonesia," ujarnya dalam audiensi dengan BIG di Kantor Kementerian Komdigi, Jakarta Pusat, Selasa (04/03/2025).

Sebagai bentuk dukungan, Kementerian Komdigi akan menyediakan infrastruktur digital yang diperlukan untuk memastikan pemanfaatan peta ini secara luas. "Kementerian Komdigi berkomitmen mendukung infrastruktur digital yang diperlukan oleh BIG untuk pengembangan Peta Digital Nasional," tambah Meutya Hafid.

Direktur Jenderal Teknologi Pemerintah Digital, Mira Tayyiba, menyoroti bahwa kebutuhan infrastruktur digital dalam penyimpanan dan pengolahan data geospasial sangat besar. Untuk itu, Kementerian Komdigi akan melakukan penilaian kebutuhan teknologi yang dibutuhkan oleh BIG, bekerja sama dengan Badan Siber dan Sandi Negara (BSSN) untuk memastikan keamanan data yang digunakan dalam peta ini.

Kepala BIG, Muh Aris Marfai, menjelaskan bahwa Peta Digital Nasional ini akan menjadi solusi strategis dalam pengembangan berbagai proyek nasional. "Dengan detail skala 1:5000, peta ini sudah dilengkapi dengan model elevasi digital yang dapat digunakan untuk berbagai sektor, mulai dari perencanaan infrastruktur hingga mitigasi bencana. Kami yakin data ini akan bermanfaat tidak hanya bagi kementerian dan lembaga, tetapi juga bagi industri di berbagai sektor," jelasnya.

Kolaborasi BIG dan Komdigi diharapkan dapat mempercepat digitalisasi dalam berbagai aspek pembangunan nasional, memastikan informasi geospasial yang lebih akurat, serta memperkuat kemandirian teknologi digital Indonesia. Dengan dukungan penuh dari berbagai pemangku kepentingan, Peta Digital Nasional ini akan menjadi landasan utama dalam mempercepat transformasi digital yang inklusif dan berkelanjutan.
"""

# Ekstraksi
keywords = extract_keywords(siaran_pers, top_n=20)
quotes = extract_quotes(siaran_pers)

# Tampilan dengan Streamlit
st.title("🔑 Kata Kunci yang Ditemukan")
st.write(", ".join(keywords))

st.title("💬 Kutipan yang Ditemukan")
st.write(quotes)

st.markdown("---")
st.markdown("**📌 Sumber: Siaran Pers BIG & Kementerian Komdigi, 04 Maret 2025**")
