from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, DateTime, func, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from src.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.users import User


class TransformedImage(Base):
    """
    Модель для збереження трансформованих зображень.

    Використовується для збереження інформації про змінені зображення,
    включаючи їх оригінальний і перетворений URL, а також дату створення.
    """

    __tablename__ = "transformed_images"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )  # Унікальний ідентифікатор трансформованого зображення

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )  # ID користувача, який виконав трансформацію

    original_url: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Оригінальний URL зображення

    transformed_url: Mapped[str] = mapped_column(
        String, nullable=False
    )  # URL трансформованого зображення

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )  # Дата створення запису

    user: Mapped["User"] = relationship(
        "User", back_populates="transformed_images", lazy="joined"
    )  # Зв’язок із користувачем
