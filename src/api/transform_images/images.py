from fastapi import APIRouter, status, HTTPException, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.repository.transformed_images import get_all_for_user, get as get_transformed_image, save as save_transformed_image
from src.models.transformed_images import TransformedImage
from src.services.qr_code import qrcode_service
from src.services.image import cloudinary_service
from src.db.database import get_db
from src.services.auth import auth_service
from src.models.users import User
from src.repository.posts import get_post
from src.core import log
from src.schemas.images import TransformResponseImageSchema

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/resize", response_model=TransformResponseImageSchema, status_code=status.HTTP_201_CREATED)
async def resize(
    post_id: UUID,
    width: int,
    height: int,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        log.error(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="post not found")
    image_url = post.image_url
    transformed_url = await cloudinary_service.resize(image_url, width, height)
    transformed_image = await save_transformed_image(user.id, post_id, transformed_url, db)
    return transformed_image

@router.post("/apply_filter", response_model=TransformResponseImageSchema, status_code=status.HTTP_201_CREATED)
async def apply_filter(
    post_id: UUID,
    width: int,
    height: int,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        log.error(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="post not found")
    image_url = post.image_url
    transformed_url = await cloudinary_service.apply_filter(image_url, width, height)
    transformed_image = await save_transformed_image(user.id, post_id, transformed_url, db)
    return transformed_image

@router.post("/reduce_size", response_model=TransformResponseImageSchema, status_code=status.HTTP_201_CREATED)
async def reduce_size(
    post_id: UUID,
    width: int,
    height: int,
    user: User = Depends(auth_service.authenticate_user),
    db: AsyncSession = Depends(get_db),
):
    post = await get_post(post_id, db)
    if not post:
        log.error(f"Post with id {post_id} not found")
        raise HTTPException(status_code=404, detail="post not found")
    image_url = post.image_url
    transformed_url = await cloudinary_service.reduce_size(image_url, width, height)
    transformed_image = await save_transformed_image(user.id, post_id, transformed_url, db)
    return transformed_image


@router.get("/user_transformed_images", response_model=list[TransformResponseImageSchema])
async def get_transformed_images_for_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    images = await get_all_for_user(user_id, db)
    if not images:
        raise HTTPException(status_code=404, detail="No transformed images found")
    return images


@router.get("/transformed_image/{image_id}", response_model=TransformResponseImageSchema)
async def get_transformed_image(image_id: UUID, db: AsyncSession = Depends(get_db)):
    image = await get_transformed_image(image_id, db)
    if not image:
        raise HTTPException(status_code=404, detail="Transform image not found")
    return image
