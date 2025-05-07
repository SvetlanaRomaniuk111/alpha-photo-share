from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CommentSchema(BaseModel):
    id: UUID
    user_id: UUID
    post_id: UUID
    message: str
    created_at: datetime
    updated_at: datetime