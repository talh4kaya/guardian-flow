from pydantic import BaseModel
from datetime import datetime

# 1. İstek Şeması (Kullanıcı ne göndermeli?)
class TransactionInput(BaseModel):
    # timestamp'i string olarak alacağız, içeride datetime'a çevireceğiz
    timestamp: str  # Örn: "2023-11-20 14:30:00"
    amount: float
    merchant: str

    class Config:
        # Swagger UI'da görünecek örnek veri
        json_schema_extra = {
            "example": {
                "timestamp": "2023-11-20 14:30:00",
                "amount": 150.50,
                "merchant": "supermarket"
            }
        }

# 2. Yanıt Şeması (Biz ne döneceğiz?)
class PredictionOutput(BaseModel):
    is_fraud: int
    probability: float
    message: str