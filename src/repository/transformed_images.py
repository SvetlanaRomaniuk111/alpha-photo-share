from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.models.transformed_images import TransformedImage

from uuid import UUID

from src.services import image

async def get_all_for_user(user_id: UUID, db: AsyncSession):
    stmt = select(TransformedImage).options(joinedload(TransformedImage.user)).filter(
        TransformedImage.user_id == user_id
    )
    result = await db.execute(stmt)

    return result.unique().scalars().all()

async def get(image_id: UUID, db: AsyncSession):
    stmt = select(TransformedImage).options(joinedload(TransformedImage.user)).filter(
        TransformedImage.id == image_id
    )
    result = await db.execute(stmt)

    return result.unique().scalar_one_or_none()

async def get_by_url(url: str, db: AsyncSession):
    stmt = select(TransformedImage).options(joinedload(TransformedImage.user)).filter(
        TransformedImage.url == url
    )
    result = await db.execute(stmt)

    return result.unique().scalar_one_or_none()

async def save(
    user_id: UUID, post_id: UUID, url: str, db: AsyncSession
) -> TransformedImage:
    new_entry = TransformedImage(
        user_id=user_id,
        post_id=post_id,
        url=url,
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry
