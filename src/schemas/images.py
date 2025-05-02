from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Any


class TransformedImageSchema(BaseModel):
    """
    Schema for storing transformed image metadata.

    Attributes:
        id (UUID): Unique identifier for the transformed image.
        original_url (HttpUrl): URL of the original uploaded image.
        transformed_url (HttpUrl): URL of the transformed image.
        created_at (datetime): Timestamp of when the transformation was applied.
    """

    id: UUID
    original_url: HttpUrl
    transformed_url: HttpUrl
    created_at: datetime

    class Config:
        from_attributes = True  # Enables compatibility with ORM models


class ImageRequestSchema(BaseModel):
    """
    Schema for requesting image transformation.

    Attributes:
        image_url (HttpUrl): URL of the image to be transformed.
        transformation (dict[str, Any]): Dictionary containing transformation parameters.
    """

    image_url: HttpUrl
    transformation: dict[str, Any]  # Allows for mixed value types (str, int, float)
