import re
import spacy
import streamlit as st

# ✅ Load model bahasa Indonesia (pastikan sudah install)
nlp = spacy.load("xx_ent_wiki_sm")  # Model multilingual dengan NER

def ekstrak_narasumber(teks):
    """ Menggunakan spaCy untuk ekstrak nama orang dari teks """
    doc = nlp(teks)
    narasumber = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return list(set(narasumber))  # Hapus duplikasi

def ekstrak_kutipan_dengan_narasumber(teks):
    """ Ekstrak kutipan lalu cocokan dengan narasumber terdekat """
    kutipan_regex = re.findall(r'[“"]([^“”]+)[”"]', teks)
    narasumber_list = ekstrak_narasumber(teks)

    kutipan_final = []
    for i, kutipan in enumerate(kutipan_regex):
        # Cari narasumber terdekat sebelum atau setelah kutipan
        before_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s*(?:ujar|kata|menurut|tambah|jelas|ungkap|papar|sebut|tegas|tandas)', teks)
        after_match = re.search(r'[“"]' + re.escape(kutipan) + r'[”"]\s*(?:ujar|kata|menurut|tambah|jelas|ungkap|papar|sebut|tegas|tandas)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', teks)

        narasumber = after_match.group(1) if after_match else (before_match.group(1) if before_match else "Tidak Diketahui")

        # Jika narasumber terdeteksi oleh spaCy tapi tidak oleh regex
        if narasumber == "Tidak Diketahui" and narasumber_list:
            narasumber = narasumber_list[0]  # Ambil kandidat pertama

        kutipan_final.append(f"{i+1}. \"{kutipan}\" - {narasumber}")

    return kutipan_final

# ✅ Input dari user
st.subheader("📝 Input Siaran Pers")
input_teks = st.text_area("Masukkan teks siaran pers di sini:")

if st.button("Ekstrak Kata Kunci & Kutipan"):
    if input_teks:
        kutipan = ekstrak_kutipan_dengan_narasumber(input_teks)

        # ✅ Kutipan dalam format pointer bernomor
        st.subheader("💬 Kutipan yang Ditemukan")
        for item in kutipan:
            st.write(item)
        
    else:
        st.warning("Masukkan teks terlebih dahulu!")

