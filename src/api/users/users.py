from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.image import ImageRequestSchema, TransformedImageSchema
from src.repository.image_repository import save_transformed_image, get_transformed_images
from src.services.image_service import transform_image, generate_qr
from src.db.database import get_db

users_router = APIRouter(prefix="/api/users", tags=["Users"])

@users_router.post("/transform", response_model=TransformedImageSchema)
async def transform_image_endpoint(body: ImageRequestSchema, db: AsyncSession = Depends(get_db)):
    try:
        transformed_url, _ = transform_image(body.image_url, body.transformation)
        qr_code_image = generate_qr(transformed_url)
        qr_code_path = f"qr_codes/{body.image_url.split('/')[-1].split('.')[0]}_qr.png"
        with open(qr_code_path, "wb") as qr_code_file:
            qr_code_image.save(qr_code_file)

        new_entry = await save_transformed_image(
            user_id=1, 
            original_url=body.image_url, 
            transformed_url=transformed_url, 
            qr_code_url=qr_code_path, 
            db=db
        )
        return new_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка трансформації: {str(e)}")

@users_router.get("/history", response_model=list[TransformedImageSchema])
async def get_transformation_history(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        history = await get_transformed_images(user_id, db)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка отримання історії: {str(e)}")