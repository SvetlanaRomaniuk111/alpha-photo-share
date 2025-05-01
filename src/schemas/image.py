from pydantic import BaseModel
from datetime import datetime

class TransformedImageSchema(BaseModel):
    original_url: str
    transformed_url: str
    qr_code_url: str
    created_at: datetime

class ImageRequestSchema(BaseModel):
    image_url: str  # Використовуємо звичайний рядок замість HttpUrl
    transformation: dict