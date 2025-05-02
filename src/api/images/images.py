from logging import config
import os
import tempfile
from fastapi import APIRouter, status, UploadFile, File
import cloudinary
from src.core.config.base_config import Settings
from src.core.config.config import cloudinary_config
from src.services.image import ImageProcessor

router = APIRouter(prefix="/images", tags=["images"])

class Cloudinary:
    @staticmethod
    def configure():
        """
        Configure Cloudinary with the credentials from the config.
        """
        cloudinary.config(
            cloud_name=cloudinary_config.CLOUDINARY_NAME,
            api_key=str(cloudinary_config.CLOUDINARY_API_KEY),  # Ensure API key is a string
            api_secret=cloudinary_config.CLOUDINARY_API_SECRET,
        )

# Configure Cloudinary at the start of the file
Cloudinary.configure()

@router.post("/upload", response_model=str, status_code=status.HTTP_201_CREATED)
async def upload_image_endpoint(file: UploadFile = File(...)):
    """
    Upload an image to Cloudinary.

    This endpoint allows users to upload an image to Cloudinary and retrieve the direct URL.

    Args:
        file (UploadFile): Image file to be uploaded.

    Returns:
        str: URL of the uploaded image.
    """
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        result = ImageProcessor.upload_image(temp_file_path)
    finally:
        os.remove(temp_file_path)  # 🔹 Ensure temporary file is deleted

    return result


@router.post("/resize", response_model=str, status_code=status.HTTP_200_OK)
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


@router.post("/filter", response_model=str, status_code=status.HTTP_200_OK)
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


@router.post("/optimize", response_model=str, status_code=status.HTTP_200_OK)
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