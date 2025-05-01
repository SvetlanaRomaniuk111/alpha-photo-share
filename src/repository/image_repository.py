from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.transformed_image import TransformedImage


async def get_transformed_images(user_id: int, db: AsyncSession):
    stmt = select(TransformedImage).filter(TransformedImage.user_id == user_id)
    result = await db.execute(stmt)
    
    return result.scalars().all()

async def save_transformed_image(user_id: int, original_url: str, transformed_url: str, qr_code_url: str, db: AsyncSession):
    new_entry = TransformedImage(
        user_id=user_id,
        original_url=original_url,
        transformed_url=transformed_url,
        qr_code_url=qr_code_url
    )
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry