
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Any

class TransformResponseImageSchema(BaseModel):
    url: HttpUrl
    post_id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ImageRequestSchema(BaseModel):
    image_url: HttpUrl
    transformation: dict[str, Any]  # Allows for mixed value types (str, int, float)
