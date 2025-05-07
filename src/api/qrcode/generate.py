from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Response, status, HTTPException, Depends
from pydantic import HttpUrl

from src.services.qr_code import qrcode_service

router = APIRouter(prefix='/qr_code', tags=['qr_code'])

@router.post("/generate_svg", status_code=status.HTTP_200_OK)
async def qr_code_svg(url: HttpUrl, size: Optional[int] = 200):
    svg_code = await qrcode_service.generateSvgAsync(url, size)
    if not svg_code:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate QR code")
    return Response(content=svg_code, media_type="image/svg+xml")

@router.post("/generate_image", status_code=status.HTTP_200_OK)
async def qr_code_image(url: HttpUrl, size: Optional[int] = 200):
    img = await qrcode_service.generatePilImageAsync(url, size)
    if not img:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate QR code")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="image/png")