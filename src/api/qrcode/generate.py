from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from src.services.qr_code import QrCodeService, qrcode_service

app = FastAPI()

class GenerateRequest(BaseModel):
    data: str
    size: Optional[int] = 200

@app.post("/qr/")
async def generate_qr(request: GenerateRequest, qr_service: QrCodeService = Depends(lambda: qrcode_service)):
    """
    Generates a QR code based on the provided data.

    Args:
        request: The request containing the data to encode and the desired size.
        qr_service: The QR code service dependency.

    Returns:
        A dictionary containing the SVG string of the QR code.
    """
    return {"svg_str": await qr_service.generateSvgAsync(request.data, request.size)}

from fastapi.responses import Response
