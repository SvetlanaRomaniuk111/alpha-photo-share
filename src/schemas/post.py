from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from sqlalchemy import String


class TagResponseSchema(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True
    }


class PostTagResponseSchema(BaseModel):
    tag: TagResponseSchema

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
    tags: Optional[List[PostTagResponseSchema]] = []

    model_config = {
        "from_attributes": True
    }

