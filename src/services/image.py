from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from fastapi import HTTPException, UploadFile
from src.core import config
import cloudinary
from cloudinary.api import delete_resources


class CloudinaryService:
    def __init__(
        self,
    ):
        self.settings = cloudinary.config(
            cloud_name=config.cloudinary_config.CLOUDINARY_NAME,
            api_key=config.cloudinary_config.CLOUDINARY_API_KEY,
            api_secret=config.cloudinary_config.CLOUDINARY_API_SECRET,
            secure=True,
        )

    public_folder = f"user_posts/"

    async def upload(self, file: UploadFile, user_email: str):
        # Завантажуємо файл до Cloudinary
        try:
            upload_result = upload(
                file.file, folder=f"{self.public_folder}{user_email}", overwrite=True
            )

            # Отримання `public_id`
            public_id = upload_result.get("public_id")
            version = upload_result.get("version")

            if not public_id:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve public_id from Cloudinary",
                )

            # Формування коректного URL
            result_url, _ = cloudinary_url(public_id, version=version)

            return result_url
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload to Cloudinary: {e}"
            )

    async def delete(self, public_id: str):
        try:
            # Удаляем конкретное изображение
            deleted_file_result = delete_resources(public_id)

            return {"deleted_file": deleted_file_result}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete image from Cloudinary: {e}"
            )


    async def resize(self, image_url: str, width: int, height: int) -> str:
        try:
            url, _ = cloudinary_url(
                image_url,
                width=width,
                height=height,
                crop="fill",
                fetch_format="auto",
                quality="auto",
            )
            return url
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to resize image: {e}"
            )

    async def apply_filter(self, image_url: str, effect: str) -> str:
        # Перевірка наявності ефекту
        if effect not in ["grayscale", "sepia", "brightness", "contrast"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid effect. Available effects: grayscale, sepia, brightness, contrast.",
            )
        url, _ = cloudinary_url(image_url, transformation=[{"effect": effect}])
        return url
    
    async def reduce_size(self, image_url: str) -> str:
        url, _ = cloudinary_url(
            image_url, quality="auto", fetch_format="auto", version="new_version"
        )
        return url

cloudinary_service = CloudinaryService()