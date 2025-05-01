from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.db.base import Base  # Використовуємо declarative_base()

class TransformedImage(Base):
    __tablename__ = "transformed_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Якщо зображення прив’язане до користувача
    original_url = Column(String, nullable=False)
    transformed_url = Column(String, nullable=False)
    qr_code_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transformed_images")  # Зв’язок з користувачем