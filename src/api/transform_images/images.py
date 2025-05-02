from fastapi import APIRouter, status, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.repository.transformed_images import get_all_for_user, get, save
from src.models.transformed_images import TransformedImage
from src.services.qrcode import qrcode_service
from src.services.image import cloudinary_service


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=str)
async def upload_image(file: UploadFile, user_email: str):
    """Загружает изображение в Cloudinary и возвращает URL."""
    return await cloudinary_service.upload(file, user_email)


@router.delete("/delete/{public_id}", response_model=dict)
async def delete_image(public_id: str):
    """Удаляет изображение из Cloudinary."""
    return await cloudinary_service.delete(public_id)


@router.post("/resize", response_model=dict, status_code=status.HTTP_200_OK)
async def resize(
    image_url: str,
    width: int,
    height: int,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Изменяет размер изображения, сохраняет его в БД и возвращает URL."""
    transformed_url = await cloudinary_service.resize(image_url, width, height)
    qr_code_url = await qrcode_service.generate_qr_code(transformed_url)

    new_entry = TransformedImage(
        user_id=user_id,
        original_url=image_url,
        transformed_url=transformed_url,
        qr_code_url=qr_code_url,
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return {"transformed_url": transformed_url, "qr_code_url": qr_code_url}


@router.post("/filter", response_model=dict, status_code=status.HTTP_200_OK)
async def apply_filter(
    image_url: str, effect: str, user_id: UUID, db: AsyncSession = Depends(get_db)
):
    """Применяет фильтр к изображению, сохраняет в БД и возвращает URL + QR-код."""
    transformed_url = await cloudinary_service.apply_filter(image_url, effect)
    qr_code_url = await qrcode_service.generate_qr_code(transformed_url)

    new_entry = TransformedImage(
        user_id=user_id,
        original_url=image_url,
        transformed_url=transformed_url,
        qr_code_url=qr_code_url,
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return {"transformed_url": transformed_url, "qr_code_url": qr_code_url}


@router.post("/reduce_size", response_model=dict, status_code=status.HTTP_200_OK)
async def reduce_size(
    image_url: str, user_id: UUID, db: AsyncSession = Depends(get_db)
):
    """Оптимизирует изображение, сохраняет результат в БД и возвращает URL + QR-код."""
    transformed_url = await cloudinary_service.reduce_size(image_url)
    qr_code_url = await qrcode_service.generate_qr_code(transformed_url)

    new_entry = TransformedImage(
        user_id=user_id,
        original_url=image_url,
        transformed_url=transformed_url,
        qr_code_url=qr_code_url,
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)

    return {"transformed_url": transformed_url, "qr_code_url": qr_code_url}


@router.get("/user/{user_id}", response_model=list)
async def get_images_for_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Получить все обработанные изображения для конкретного пользователя."""
    images = await get_all_for_user(user_id, db)
    if not images:
        raise HTTPException(status_code=404, detail="Изображения не найдены")
    return images


@router.get("/{image_id}", response_model=dict)
async def get_image(image_id: UUID, db: AsyncSession = Depends(get_db)):
    """Получить одно обработанное изображение по его ID."""
    image = await get(image_id, db)
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return image


@router.get("/qr/{image_id}", response_model=str)
async def get_qr_code(image_id: UUID, db: AsyncSession = Depends(get_db)):
    """Отримати QR-код для трансформованого зображення."""
    image = await get(image_id, db)
    if not image or not image.qr_code_url:
        raise HTTPException(status_code=404, detail="QR-код не знайдено")
    return image.qr_code_url
