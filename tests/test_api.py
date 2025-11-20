import pytest
from fastapi.testclient import TestClient
from src.api.main import app

# @pytest.fixture: Bu bir "Kurulum" fonksiyonudur.
# Testler başlamadan önce çalışır, client'ı hazırlar ve testlere gönderir.
@pytest.fixture(scope="module")
def client():
    # "with" bloğu, lifespan (startup) eventlerini tetikler!
    # Yani modeli hafızaya yükler.
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Health check endpoint'i çalışıyor mu?"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"
    # Modelin yüklendiğini de kontrol edelim
    assert response.json()["model_loaded"] is True

def test_prediction_normal(client):
    """Normal bir işlem güvenli olarak tahmin ediliyor mu?"""
    payload = {
        "timestamp": "2023-11-20 10:00:00",
        "amount": 50.0,
        "merchant": "supermarket"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["is_fraud"] == 0

def test_prediction_fraud(client):
    """Yüksek tutarlı işlem fraud olarak yakalanıyor mu?"""
    payload = {
        "timestamp": "2023-11-20 03:00:00",
        "amount": 10000.0,
        "merchant": "jewelry"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["is_fraud"] == 1