# 🛡️ Guardian-Flow: Real-Time Fraud Detection System

![CI Pipeline](https://github.com/talh4kaya/guardian-flow/actions/workflows/tests.yaml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Container-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Guardian-Flow, finansal işlemleri analiz ederek sahtecilik (fraud) girişimlerini gerçek zamanlı olarak tespit eden, uçtan uca End-to-End bir MLOps projesidir.

Bu proje; veri üretiminden model eğitimine, Dockerizasyondan CI/CD süreçlerine kadar modern yazılım mühendisliği ve veri bilimi prensiplerini (MLOps) birleştirir.

## Proje Mimarisi & Özellikler

Bu proje sadece bir modelden ibaret değildir, yaşayan bir sistemdir:

* ** Sentetik Veri Üretimi:** Gerçekçi ve dengesiz (imbalanced) finansal veri simülasyonu.
* ** pipeline:** Scikit-Learn Pipeline ile veri işleme ve modelleme bütünlüğü.
* ** Model:** Random Forest algoritması ile eğitilmiş, yüksek duyarlılıklı (Recall odaklı) sınıflandırıcı.
* ** API Serving:** FastAPI ile asenkron tahmin servisi.
* ** Docker:** Her ortamda çalışabilen izole konteyner yapısı.
* ** CI/CD:** GitHub Actions ile otomatik test ve entegrasyon süreçleri.

```bash
##  Proje Yapısı
guardian-flow/
├── .github/workflows/   # CI/CD Pipeline (GitHub Actions)
├── data/                # Veri setleri (Git-ignored)
├── models/              # Eğitilmiş modeller (.joblib)
├── notebooks/           # Keşifsel Veri Analizi (EDA)
├── src/                 # Kaynak Kodlar
│   ├── api/             # FastAPI Uygulaması
│   ├── data/            # Veri işleme scriptleri
│   └── models/          # Model eğitim scriptleri
├── tests/               # Unit Testler
├── Dockerfile           # Docker imaj dosyası
└── requirements.txt     # Bağımlılıklar




🛠 Kurulum ve Çalıştırma
Projeyi lokalinizde çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

Yöntem 1: Docker ile
Bilgisayarınızda Python kurulu olmasına gerek yok, sadece Docker yeterli.

# 1. İmajı oluştur
docker build -t guardian-flow .

# 2. Konteyneri başlat
docker run -p 8000:8000 guardian-flow
Yöntem 2: Lokal Python Ortamı ile

# 1. Repoyu klonla
git clone [https://github.com/talh4kaya/guardian-flow.git](https://github.com/talh4kaya/guardian-flow.git)
cd guardian-flow

# 2. Sanal ortamı kur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. API'yi başlat
uvicorn src.api.main:app --reload
API Kullanımı
Sistem ayağa kalktıktan sonra Swagger arayüzüne şuradan erişebilirsiniz: 👉 http://localhost:8000/docs

Örnek Tahmin İsteği (JSON)
JSON
{
  "timestamp": "2023-11-20 14:30:00",
  "amount": 5000.0,
  "merchant": "jewelry"
}

Beklenen Yanıt:
JSON
{
  "is_fraud": 1,
  "probability": 0.95,
  "message": "RİSKLİ İŞLEM TESPİT EDİLDİ!"
}

Testler
Test senaryolarını çalıştırmak için:
pytest