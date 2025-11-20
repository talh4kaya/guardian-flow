# 1. Taban İmaj (Python 3.9 yüklü hafif bir Linux)
FROM python:3.9-slim

# 2. Çalışma dizinini ayarla
WORKDIR /app

# 3. Önce gereksinimleri kopyala (Cache avantajı için)
COPY requirements.txt .

# 4. Kütüphaneleri yükle
# --no-cache-dir: İmaj boyutunu şişirmemek için önbellek tutma
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kaynak kodları ve modeli kopyala
COPY src/ src/
COPY models/ models/
# (Data klasörünü kopyalamıyoruz, modele ve koda ihtiyacımız var)

# 6. Çevresel değişken (Python çıktıları anında görünsün diye)
ENV PYTHONUNBUFFERED=1

# 7. Konteynerin dışarıya açacağı port
EXPOSE 8000

# 8. Başlatma komutu
# host 0.0.0.0 olmak ZORUNDA (Yoksa dışarıdan erişilemez)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]