from fastapi import APIRouter, status
from src.services.image import ImageProcessor

users_router = APIRouter(prefix="/api/users", tags=["Users"])


@users_router.post("/upload", response_model=str, status_code=status.HTTP_201_CREATED)
async def upload_image_endpoint(file_path: str):
    """
    Upload an image to Cloudinary.

    This endpoint allows users to upload an image to Cloudinary and retrieve the direct URL.

    Args:
        file_path (str): Path to the image file to be uploaded.

    Returns:
        str: URL of the uploaded image.
    """
    return ImageProcessor.upload_image(file_path)


@users_router.post("/resize", response_model=str, status_code=status.HTTP_200_OK)
async def resize_image_endpoint(image_url: str, width: int, height: int):
    """
    Resize an image using Cloudinary.

    Users can specify the width and height to scale the image.

    Args:
        image_url (str): URL of the original image.
        width (int): Desired width of the resized image.
        height (int): Desired height of the resized image.

    Returns:
        str: URL of the resized image.
    """
    return ImageProcessor.resize_image(image_url, width, height)


@users_router.post("/filter", response_model=str, status_code=status.HTTP_200_OK)
async def apply_filter_endpoint(image_url: str, effect: str):
    """
    Apply a filter/effect to an image.

    Users can add various effects such as grayscale, sepia, etc.

    Args:
        image_url (str): URL of the original image.
        effect (str): Name of the effect to be applied.

    Returns:
        str: URL of the filtered image.
    """
    return ImageProcessor.apply_filter(image_url, effect)


@users_router.post("/optimize", response_model=str, status_code=status.HTTP_200_OK)
async def optimize_image_endpoint(image_url: str):
    """
    Optimize an image to reduce file size while maintaining quality.

    This endpoint ensures images are delivered in the best format for performance.

    Args:
        image_url (str): URL of the original image.

    Returns:
        str: URL of the optimized image.
    """
    return ImageProcessor.optimize_image(image_url)
