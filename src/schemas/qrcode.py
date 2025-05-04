from typing import Optional
from pydantic import BaseModel

class QrcodeResponseSchema(BaseModel):
    data: str
    size: Optional[int] = 200