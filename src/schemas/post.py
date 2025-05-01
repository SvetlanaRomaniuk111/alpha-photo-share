from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy Post model
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)


# Pydantic schemas
class PostCreationSchema(BaseModel):
    title: str = Field(String, nullable=False, min_length=3, max_length=30, )
    description: str = Field(String, nullable=False,min_length=3, max_length=250)
    image_url: str = Field(String, nullable=False, min_length=3, max_length=100)

    class Config:
        orm_mode = True


class PostUpdateSchema(BaseModel):
    title: Optional[str] = Field(String, nullable=False,min_length=3, max_length=30)
    description: Optional[str] = Field(String, nullable=False,min_length=3, max_length=250)
    image_url: Optional[str] = Field(String, nullable=False,min_length=3, max_length=100)

    class Config:
        orm_mode = True


class PostResponse(BaseModel):

    id: UUID
    user_id: UUID
    title: str
    description: str
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True