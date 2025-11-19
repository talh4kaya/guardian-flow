import pandas as pd
import os

def load_data(path):
    """Ham veriyi okur"""
    # TODO: pd.read_csv ile veriyi oku ve döndür
    return pd.read_csv(path)

def feature_engineering(df):
    """
    Ham veriden yeni özellikler türetir (Notebook'ta yaptıkların).
    """
    df = df.copy()
    
    # Datetime dönüşümü (Hata almamak için)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # TODO 1: 'hour' kolonunu oluştur
    df['hour'] = df['timestamp'].dt.hour
    
    # TODO 2: 'day_of_week' kolonunu oluştur (0: Pzt, 6: Paz)
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # TODO 3: 'is_weekend' kolonu ekle (Ctesi veya Pazar ise 1)
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    return df

def clean_data(df):
    """Gereksiz kolonları atar"""
    cols_to_drop = ['customer_id', 'timestamp']
    
    # TODO 4: drop fonksiyonu ile bu kolonları sil.
    df = df.drop(columns=cols_to_drop)
    
    return df

def save_processed_data(df, output_path):
    """İşlenmiş veriyi kaydeder"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # TODO 5: index=False ile kaydet
    df.to_csv(output_path, index=False)

def main():
    raw_data_path = "data/raw/transactions.csv"
    processed_data_path = "data/processed/train_data.csv"
    
    print("🚀 Veri işleme başlıyor...")
    
    # 1. Yükle
    df = load_data(raw_data_path)
    
    # 2. Feature Engineering
    df = feature_engineering(df)
    
    # 3. Temizle
    df = clean_data(df)
    
    # 4. Kaydet
    save_processed_data(df, processed_data_path)
    
    print(f"✅ İşlenmiş veri kaydedildi: {processed_data_path}")
    print(f"Son Boyut: {df.shape}")
    print(df.head())

if __name__ == "__main__":
    main()
