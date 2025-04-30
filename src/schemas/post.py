from typing import Optional
from uuid import UUID

from pydantic import BaseModel,  Field
from datetime import datetime


class PostSchema(BaseModel):
    title: str = Field( min_length=3, max_length=30)
    description: str = Field( min_length=3, max_length=250)
    image_url: str = Field(min_length=3, max_length=100)



class PostUpdateSchema(BaseModel):
    title: str = Field( min_length=3, max_length=30)
    description: str = Field( min_length=3, max_length=250)
    image_url: str = Field(min_length=3, max_length=100)



class PostResponse(BaseModel):

    id: UUID
    user_id: UUID
    title: str
    description: str
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True