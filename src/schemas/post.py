from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from sqlalchemy import String


# Pydantic post schemas
class PostUpdateSchema(BaseModel):
    title: Optional[str] = Field(String, nullable=False,min_length=3, max_length=30)
    description: Optional[str] = Field(String, nullable=False,min_length=3, max_length=250)
    
    model_config = {
        "from_attributes": True
    }


class PostResponseSchema(BaseModel):

    id: UUID
    user_id: UUID
    title: str
    description: str
    image_url: HttpUrl 
    created_at: datetime
    updated_at: datetime
    tags: Optional[list[str]] = Field(default=[])

    model_config = {
        "from_attributes": True
    }


