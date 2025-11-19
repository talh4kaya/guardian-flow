# src/data/make_dataset.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# AYARLAR
NUM_SAMPLES = 10000
FRAUD_RATIO = 0.05  # %5 Fraud
RANDOM_SEED = 42

# Her çalıştırdığımızda aynı veriyi üretmesi için
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

def generate_customer_data(num_customers=1000):
    """
    Rastgele müşteri ID'leri üretir.
    Örn Çıktı: ['CUST_001', 'CUST_002', ...]
    """
    print(f"{num_customers} adet müşteri ID'si üretiliyor...")
    
    # TODO 1: List comprehension kullanarak CUST_0001 formatında ID'ler oluştur.
    customer_ids = [f"CUST_{i:04d}" for i in range(1, num_customers + 1)]
    
    return customer_ids

def generate_transactions(num_samples):
    """
    Sentetik işlem verisi üretir.
    """
    print("İşlem verileri ve zaman damgaları oluşturuluyor...")
    
    # Müşteri listesini al
    customers = generate_customer_data()
    
    # 1. Zaman damgaları (Son 30 gün)
    base_date = datetime.now()
    timestamps = [base_date - timedelta(minutes=x) for x in range(num_samples)]
    
    # 2. Müşteri Seçimi
    # TODO 2: Rastgele müşteri seçimi
    selected_customers = np.random.choice(customers, size=num_samples, replace=True)
    
    # 3. İşlem Tutarları
    amounts = np.random.normal(50, 10, num_samples)
    amounts = np.abs(amounts)
    
    # 4. Kategori Seçimi
    categories = ['supermarket', 'electronics', 'gas_station', 'online_subscription', 'jewelry']
    # TODO 3: Rastgele kategori seçimi
    selected_categories = np.random.choice(categories, size=num_samples, replace=True)
    
    # 5. Fraud Etiketleme
    labels = np.zeros(num_samples, dtype=int)
    num_frauds = int(num_samples * FRAUD_RATIO)
    fraud_indices = np.random.choice(num_samples, size=num_frauds, replace=False)
    labels[fraud_indices] = 1
    
    # 6. Fraud Senaryosu — Fraud olan işlemleri daha büyük yapalım
    # TODO 4: Fraud olan indexlerde amount'u artır
    amounts[fraud_indices] *= 5  # Fraud işlemler 5 kat daha büyük
    
    # DataFrame oluşturma
    df = pd.DataFrame({
        'timestamp': timestamps,
        'customer_id': selected_customers,
        'merchant': selected_categories,
        'amount': amounts,
        'is_fraud': labels
    })
    
    return df

def save_data(df, path):
    """Veriyi CSV olarak kaydeder"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # TODO 5: CSV kaydet
    df.to_csv(path, index=False)

if __name__ == "__main__":
    df = generate_transactions(NUM_SAMPLES)
    
    save_path = "data/raw/transactions.csv"
    save_data(df, save_path)
    
    print(f"✅ Veri seti oluşturuldu: {save_path}")
    print(df.head())
    print(df['is_fraud'].value_counts())
# Bu bir git test yorumudur.