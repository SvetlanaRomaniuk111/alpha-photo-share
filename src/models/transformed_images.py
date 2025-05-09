from httpx import post
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, DateTime, func, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from src.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .posts import Post


class TransformedImage(Base):
    __tablename__ = "transformed_images"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )  # Унікальний ідентифікатор трансформованого зображення

    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )  # ID поста, до якого належить трансформоване зображення

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )  # ID користувача, який виконав трансформацію

    url: Mapped[str] = mapped_column(
        String, nullable=False
    )  # URL трансформованого зображення

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )  # Дата створення запису

    user: Mapped["User"] = relationship(
        "User", back_populates="transformed_images", lazy="joined"
    )

    post: Mapped["Post"] = relationship(
        "Post", back_populates="transformed_images", lazy="joined"
    )  # Відношення до моделі Post
