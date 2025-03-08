import os
import spacy

MODEL_PATH = "id_core_news_sm"

# ✅ Cek apakah model sudah ada sebelum dipanggil
try:
    nlp = spacy.load(MODEL_PATH)
    spacy_status = "✅ Model SpaCy IndoNLP berhasil dimuat!"
except OSError:
    os.system(f"python -m spacy download {MODEL_PATH}")
    try:
        nlp = spacy.load(MODEL_PATH)
        spacy_status = "✅ Model SpaCy IndoNLP berhasil dimuat setelah instalasi!"
    except OSError:
        nlp = None
        spacy_status = "❌ Model SpaCy gagal diinstal!"

