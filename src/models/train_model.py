import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os

# AYARLAR
PROCESSED_DATA_PATH = "data/processed/train_data.csv"
MODEL_PATH = "models/model_pipeline.joblib"
RANDOM_STATE = 42

def load_data(path):
    """İşlenmiş veriyi yükler"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Veri bulunamadı: {path}")
    return pd.read_csv(path)

def build_pipeline():
    """Pipeline iskeletini kurar (Parametreler GridSearch'ten gelecek)"""
    categorical_features = ['merchant']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=RANDOM_STATE, class_weight='balanced'))
    ])
    
    return pipeline

def optimize_model(pipeline, X_train, y_train):
    """Grid Search ile en iyi parametreleri bulur"""
    print("🔍 Hyperparameter Tuning başlatılıyor...")
    
    # Denenecek parametreler
    # Not: Pipeline içindeki isme 'classifier__' ön ekiyle ulaşırız.
    param_grid = {
        'classifier__n_estimators': [50, 100, 200],     # Ağaç sayısı
        'classifier__max_depth': [None, 10, 20],        # Ağaç derinliği
        'classifier__min_samples_split': [2, 5]         # Bölünme kriteri
    }
    
    # 3-Katlı Çapraz Doğrulama (3-Fold Cross Validation)
    grid_search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=3, 
        scoring='recall', # Fraud yakalamak öncelikli olduğu için 'recall' seçtik
        n_jobs=-1,        # Tüm işlemci çekirdeklerini kullan
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"🏆 En İyi Parametreler: {grid_search.best_params_}")
    print(f"🌟 En İyi Skor (Recall): {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_

def train_and_evaluate(df):
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    # Stratified Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    
    # Pipeline Kurulumu
    base_pipeline = build_pipeline()
    
    # Optimizasyon (Grid Search)
    # Normalde .fit() derdik, şimdi optimize_model diyoruz
    best_model = optimize_model(base_pipeline, X_train, y_train)
    
    # Test
    print("\n🔮 Test Seti Üzerinde Performans:")
    y_pred = best_model.predict(X_test)
    
    print(classification_report(y_test, y_pred))
    
    return best_model

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"✅ Optimize edilmiş model kaydedildi: {path}")

if __name__ == "__main__":
    df = load_data(PROCESSED_DATA_PATH)
    trained_model = train_and_evaluate(df)
    save_model(trained_model, MODEL_PATH)