from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from src.services.qr_code import QrCodeService, qrcode_service

app = FastAPI()

class GenerateRequest(BaseModel):
    data: str
    size: Optional[int] = 200

qr_codes = {}
key_counter = 0

@app.post("/qr/")
async def generate_qr(request: GenerateRequest, qr_service: QrCodeService = Depends(lambda: qrcode_service)):
    """
    Generates a QR code based on the provided data and stores it.

    Args:
        request (GenerateRequest): The request containing the data to encode and the desired size.
        qr_service (QrCodeService): The QR code service dependency.

    Returns:
        dict: A dictionary containing the key to retrieve the QR code.
    """
    global key_counter
    key = str(key_counter)
    key_counter += 1
    qr_codes[key] = await qr_service.generateSvgAsync(request.data, request.size)
    return {"key": key}

@app.get("/qr/{key}")
async def get_qr(key: str):
    """
    Retrieves a QR code based on the provided key.

    Args:
        key (str): The key of the QR code to retrieve.

    Returns:
        Response: An SVG image of the QR code.

    Raises:
        HTTPException: If the QR code with the given key is not found.
    """
    if key not in qr_codes:
        raise HTTPException(status_code=404, detail="QR code not found")
    return Response(content=qr_codes[key], media_type="image/svg+xml")

from fastapi.responses import Response
