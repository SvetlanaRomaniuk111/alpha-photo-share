from typing import Optional

from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import HttpUrl

from src.schemas.qrcode import QrcodeResponseSchema
from src.services.qr_code import qrcode_service

router = APIRouter(prefix='/qr', tags=['qr'])

@router.post("/generate", response_model=QrcodeResponseSchema, status_code=status.HTTP_200_OK)
async def generate_qr_code(url: HttpUrl, size: Optional[int] = 200):
    return await qrcode_service.generateSvgAsync(url, size)
