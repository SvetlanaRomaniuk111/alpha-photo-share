from fastapi import APIRouter, status
from src.services.image import cloudinary_service

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/resize", response_model=str, status_code=status.HTTP_200_OK)
async def resize(image_url: str, width: int, height: int):
    return cloudinary_service.resize(image_url, width, height)


@router.post("/filter", response_model=str, status_code=status.HTTP_200_OK)
async def apply_filter(image_url: str, effect: str):
    return cloudinary_service.apply_filter(image_url, effect)


@router.post("/reduce_size", response_model=str, status_code=status.HTTP_200_OK)
async def reduce_size(image_url: str):
    return cloudinary_service.reduce_size(image_url)
