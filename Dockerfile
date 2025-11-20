# 1. Taban İmaj
FROM python:3.9-slim

# 2. Çalışma dizini
WORKDIR /app

# 3. Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Kaynak kodları kopyala
COPY src/ src/

# 5. Gerekli klasörleri oluştur (Garanti olsun)
RUN mkdir -p models data/raw data/processed

# ---------------------------------------------------
# 🛠 KRİTİK HAMLE: MODELİ BURADA SIFIRDAN EĞİTİYORUZ
# ---------------------------------------------------

# A) Sentetik veriyi üret
RUN python src/data/make_dataset.py

# B) Veriyi işle (Feature Engineering)
RUN python src/data/preprocess.py

# C) Modeli eğit ve kaydet (models/model_pipeline.joblib oluşacak)
RUN python src/models/train_model.py

# ---------------------------------------------------

# 6. Çevresel değişkenler
ENV PYTHONUNBUFFERED=1

# 7. Portu dışarı aç
EXPOSE 8000

# 8. Başlat
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]