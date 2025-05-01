from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text
from sqlalchemy.ext.declarative import declarative_base


# Pydantic schemas
class PostCreationSchema(BaseModel):
    title: str = Field(String, nullable=False, min_length=3, max_length=30, )
    description: str = Field(String, nullable=False,min_length=3, max_length=250)
    image_url: HttpUrl  = Field(String, nullable=False, min_length=3, max_length=100)

    model_config = {
        "from_attributes": True
    }


class PostUpdateSchema(BaseModel):
    title: Optional[str] = Field(String, nullable=False,min_length=3, max_length=30)
    description: Optional[str] = Field(String, nullable=False,min_length=3, max_length=250)
    image_url: Optional[HttpUrl] = Field(String, nullable=False,min_length=3, max_length=100)     
    
    model_config = {
        "from_attributes": True
    }


class PostResponse(BaseModel):

    id: UUID
    user_id: UUID
    title: str
    description: str
    image_url: HttpUrl 
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }