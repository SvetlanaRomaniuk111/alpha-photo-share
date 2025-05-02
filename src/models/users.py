import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, String, Integer, DateTime, ForeignKey, Enum, func, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.posts import Post
    from src.models.image import TransformedImage


class Role(str, enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class Gender(str, enum.Enum):
    M = "M"
    F = "F"


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    age: Mapped[int] = mapped_column(Integer(), nullable=False)
    gender: Mapped[Enum] = mapped_column("gender", Enum(Gender), nullable=False)

    transformed_images: Mapped[list["TransformedImage"]] = relationship(
        "TransformedImage", back_populates="user", lazy="joined"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    role: Mapped[Enum] = mapped_column(
        "role", Enum(Role), nullable=False, default=Role.user
    )

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", lazy="joined")
