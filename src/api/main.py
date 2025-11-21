from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from .schemas import PredictionOutput, TransactionInput

# Global değişken (Model hafızada burada tutulacak)
model_pipeline = None


# Yaşam Döngüsü (Lifespan): Uygulama açılırken modeli yükle, kapanırken temizle.
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_pipeline
    # Modeli yükle
    model_path = "models/model_pipeline.joblib"
    try:
        model_pipeline = joblib.load(model_path)
        print(f"✅ Model başarıyla yüklendi: {model_path}")
    except Exception as e:
        print(f"🚨 Model yüklenemedi! Hata: {e}")
        # Gerçek hayatta burada uygulamayı durdururuz

    yield

    # Uygulama kapanırken yapılacaklar (Varsa veritabanı bağlantısını kes vs.)
    print("🛑 Uygulama kapatılıyor...")
    model_pipeline = None


# Uygulamayı başlat
app = FastAPI(title="Guardian-Flow Fraud Detection API", lifespan=lifespan)


@app.get("/")
def health_check():
    return {"status": "running", "model_loaded": model_pipeline is not None}


@app.post("/predict", response_model=PredictionOutput)
def predict(transaction: TransactionInput):

    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Model henüz yüklenmedi.")

    try:
        # 1. Gelen veriyi DataFrame'e çevir (Modelin beklediği format)
        # Pydantic modelini dict'e, oradan DataFrame'e çeviriyoruz
        data = pd.DataFrame([transaction.dict()])

        # 2. Preprocessing (Pipeline içinde otomatik yapılıyor ama format dönüşümü lazım)
        # Tarih string geldi, onu datetime objesine çevirmeliyiz (Preprocess kodundaki gibi)
        # NOT: Normalde preprocess kodunu buraya import etmek en doğrusudur ama
        # pipeline'ımızda ColumnTransformer var, tarih parçalamayı (hour, day) manuel yapmıştık.
        # O yüzden basit bir feature extraction'ı burada anlık yapalım:

        data["timestamp"] = pd.to_datetime(data["timestamp"])
        data["hour"] = data["timestamp"].dt.hour
        data["day_of_week"] = data["timestamp"].dt.dayofweek
        data["is_weekend"] = data["day_of_week"].isin([5, 6]).astype(int)

        # Gereksiz timestamp kolonunu at (Model eğitimi sırasında pipeline'a girmeden atmıştık)
        data = data.drop(columns=["timestamp"])

        # 3. Tahmin
        prediction = model_pipeline.predict(data)[0]
        probs = model_pipeline.predict_proba(data)[
            0
        ]  # [Olasılık_Normal, Olasılık_Fraud]
        fraud_prob = probs[1]

        # 4. Yanıt Dön
        return {
            "is_fraud": int(prediction),
            "probability": float(fraud_prob),
            "message": (
                "RİSKLİ İŞLEM TESPİT EDİLDİ!" if prediction == 1 else "İşlem Güvenli"
            ),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
