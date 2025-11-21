from locust import HttpUser, task, between
import random

class FraudTestUser(HttpUser):
    # Her bir kullanıcı (bot), bir işlem yaptıktan sonra 1 ile 3 saniye arası bekler.
    # (Gerçek insan taklidi yapmak için)
    wait_time = between(1, 3)

    @task
    def predict_transaction(self):
        """API'ye sürekli tahmin isteği gönderir"""
        
        # Her istekte farklı veri gönderelim ki sunucu önbellekten (cache) yemesin.
        payload = {
            "timestamp": "2023-11-20 14:30:00",
            "amount": random.randint(10, 20000), # Rastgele tutar
            "merchant": random.choice(["supermarket", "jewelry", "electronics", "gas_station"])
        }
        
        # POST isteğini yap
        # /predict adresine istek atıyoruz (Ana domaini arayüzden gireceğiz)
        self.client.post("/predict", json=payload)