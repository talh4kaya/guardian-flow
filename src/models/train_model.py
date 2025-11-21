import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# AYARLAR
PROCESSED_DATA_PATH = "data/processed/train_data.csv"
MODEL_PATH = "models/model_pipeline.joblib"
RANDOM_STATE = 42


def load_data(path):
    """İşlenmiş veriyi yükler"""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Veri bulunamadı: {path}. Önce preprocess.py çalıştırılmalı!"
        )
    return pd.read_csv(path)


def build_pipeline():
    """
    Ön işleme ve modelleme adımlarını içeren Pipeline'ı kurar.
    """
    categorical_features = ["merchant"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=100, random_state=RANDOM_STATE, class_weight="balanced"
                ),
            ),
        ]
    )

    return pipeline


def train_and_evaluate(df):
    """Modeli eğitir ve sonuçları raporlar"""

    X = df.drop("is_fraud", axis=1)
    y = df["is_fraud"]

    # TODO 1 ÇÖZÜLDÜ ✔
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    print("🛠 Pipeline kuruluyor...")
    model_pipeline = build_pipeline()

    print("🏋️ Model eğitiliyor...")
    # TODO 2 ÇÖZÜLDÜ ✔
    model_pipeline.fit(X_train, y_train)

    print("🔮 Test verisi üzerinde tahmin yapılıyor...")
    # TODO 3 ÇÖZÜLDÜ ✔
    y_pred = model_pipeline.predict(X_test)

    print("\n📊 MODEL PERFORMANS RAPORU")
    print("-" * 30)
    print(classification_report(y_test, y_pred))
    print("-" * 30)

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model_pipeline


def save_model(model, path):
    """Modeli diske kaydeder"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # TODO 4 ÇÖZÜLDÜ ✔
    joblib.dump(model, path)


if __name__ == "__main__":
    print("🚀 Model eğitim süreci başladı...")

    df = load_data(PROCESSED_DATA_PATH)
    trained_model = train_and_evaluate(df)

    save_model(trained_model, MODEL_PATH)
    print(f"\n✅ Model başarıyla kaydedildi: {MODEL_PATH}")
